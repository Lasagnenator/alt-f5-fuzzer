# Alt-F5 Fuzzer

## Description
This project aims to be a fuzzer for programs that take in data from stdin and
will attempt to crash that program in a meaninful way that could potentially be
exploited.

## Installation
This fuzzer is written in Python 3 and runs on a Linux operating system.

1. Installing dependencies
   `./install.sh`
2. Clone the repository

## Usage
The general usage of the fuzzer is `./fuzzer <binary> <sample input>`. The binary
should be marked as executable. Sample input should be a file containing non-crashing
input to the binary.

## Functionality

Our fuzzer design consists of three components. Firstly, there is a setup component which contains a format finder and prepares the binary. Next we alter the sample text using various mutation strategies. Finally, we test our mutated input against the program.

### Setup
Our setup starts with a format finder which simply takes in the given sample input for the program and runs some basic tests on them to try and determine the format of the input (i.e. csv, json, xml etc). This is used in the next step to determine which file specific mutators we should utilise. After this the binary is examined to find all the addresses of conditional jump instructions and their two paths in order to be used for measuring coverage during the testing input phase of fuzzing. The way we will later measure how much of the binary has been explored (a.k.a. coverage) is by using gdb. For this, we use the addresses of conditional jumps we just found and feed it to gdb as breakpoints. However, we don't want to actually stop at them, but instead just record that we touched those addresses. As such, commands to continue are also added to the breakpoints.

### Mutation
Mutation of the sample input to create a new input is done using numerous mutators. These mutators take in a byte string and mutate it in a specific way (depending on which mutator it is) according to a vector which is given as input. These vectors are generated using the scipy optimisation package with feedback from prior results and is explained in depth in the ‘Something Awesome’ section.

There are specific mutators for each type of format as well as a generic plaintext one which can operate on any selection of bytes. Within each format’s strategy there are many sub-mutators. Plaintext has 4: repeated input, substring selection, bit flips and byte flips. Json contains 7: integer corruption, extreme integer values, float infinities, float nans, repeated lists, repeated entries and type changes. CSV has 7 as well: repeated rows, empty rows, repeated columns, empty columns, missing header, cell multiplication and missing cells. XML has 6 mutation strategies: very deep nesting of tags, repeated attributes, href attribute corruption, tag repetition, root tag manipulation and repeated children. JPEG has 6 strategies: changed filename, changed size, changed width, changed height, metadata bit flips and metadata byte flips (since bit flips on the pixels are almost always useless). The ELF and PDF strategies are combined because they operate very closely to one another. They use byte insertion, byte replacement, byte appending byte shuffles and repetition.

### Testing Inputs

Finally, there is the testing component of the fuzzer. Firstly, there are a handful of quick simple cases that can be done separately to test for very specific types of exploits as seen in the try_simple function. Next, the fuzzer starts up many threads (limit based on cpu count) with each one having different tasks to carry out. Half of the threads are dedicated to just trying many mutation strategies as fast as possible in the allocated 180 seconds. The last group of threads work with gdb to change their mutations based on the branch coverage of their inputs. Then there is some code to count up the breakpoints that were hit in order to measure this. The program will then use this to help the scipy.optimize.minimize function to guide the exploration of inputs as detailed in the ‘Something Awesome’ section. For each attempt of input there is a check at the end for the return code. If this is not 0 or 1, bad.txt is written with the offending input. Care has been taken to kill the fuzzer almost instantly in this case and to not allow multiple writers to the file.

### Timeouts
All aspects of the fuzzer internals include timeouts in order to make sure that nothing gets stuck at some points. Runs utilising coverage timeout after just 5 seconds, whereas other runs (such as try_simple) timeout after 1 second. The relatively short timeouts combined with multithreading allows the fuzzer to attempt many different strategies without much compromise in the allotted 180 seconds. It should also be noted that the number of threads chosen aims to saturate the available cpu power and it is unlikely that other background programs will be very usable during this time. To detect infinite loops, the simple approach of timeouts are used for two reasons. For starters, the timeout duration is short so it is unlikely that too much time would be lost (at most 5 seconds on one of our threads). The main reason is checking coverage constantly to see if there is an infinite loop would add significant overheads to the program and reduce its running time. While we might slightly save a small amount of time on runs where there are infinite loops, the cost of the overheads on all the other runs make timeouts the far more efficient strategy for infinite loop detection.

### Statistics Collection and Display
Each mutator strategy comes with a human readable description of what it does. When an offending input is discovered, the strategy that produced it is displayed to the user with details on the order of operations performed to make it happen. The gdb led mutation strategy also prints out its progress with the breakpoint 'score'. The higher this score is, the more code paths that were taken in the binary.

### Types of Detectable Vulnerabilities
Our fuzzer can easily find trivial bugs like long inputs, empty files or injected big integer values. Our mutation strategies let it find bugs of many more kinds which are often unique to the specific program. Anything which could be triggered by a specific input changing or being altered (for example something program specific which requires a value to be a specific value) can be found. Each file type also has specific types of vulnerabilities which can be detected. For a detailed list of vulnerabilities which can be found, refer to our mutation strategies. Our fuzzer can hunt specifically for bugs which are buried quite deeply. The use of our breakpoint ‘score’ allows the fuzzer to figure out deep nested conditions that might be the source of bugs.

### Potential Improvements
One thing that our fuzzer does not do is have fine details for the cause of crashes when it is a coverage or non-coverage led strategy. This would require relating input vectors to what changes are made into a human readable format which seems very difficult to do, but could provide much better feedback to the user.

Our breakpoint and coverage measurements can also take an awfully long time. This is because we don't have the source code available to then inject coverage data directly. Instead we use gdb's software breakpoints, but these cause very significant overheads. A much more efficient way to implement code coverage into the fuzzer would be to directly compile in coverage instructions to the source code. This would avoid the massive overheads caused by gdb’s software breakpoints. One way to achieve this without source code would be to decompile the binary into an exact representation, inject coverage code and then recompile it. Such an implementation would greatly help our fuzzer, but would also require much more effort than a small project on our scale asks for.

### Something Awesome!

For our ‘something awesome’ we decided to utilise machine learning style based mathematical optimisation functions in order to guide our fuzzer into finding successful mutations which test as much of the code as possible. The Python package ‘scipy’ contains these mathematical optimisation functions which utilise machine learning principles to minimise or maximise a function. The question for us was how could we possibly utilise such a framework in order to find a vulnerability in a program?

The scipy.optimize.minimize function takes in a starting vector as an input, as well as a means for evaluating its output. It then optimises the vector to provide a minimal output. In our program, a vector is evaluated by using it as an input for mutators and then measuring the code coverage when the mutated input is wrong. A higher code coverage produces a lower value. Scipy will thus keep changing the vector in a way that it increases code coverage using its optimisation techniques.

In order for scipy’s optimisation techniques to actually be able to find improvements, we had to make a few design choices. Firstly, the mutators had to be deterministic in their output since otherwise the output of a vector would not be clearly related to the vector choice. Our mutators had to also be ‘linearised’ in the sense that a small change in the vector would result in a small change in the output (avoiding avalanche effects like those from hashes). Another factor was that scipy works in floats and vectors, not the integer parameters that were usually required for mutation. As such we had to provide a form of conversion from the vector to the integer parameters we needed. All of these properties combined allowed us to use the scipy library to properly optimise the coverage.

The choice of coverage was an obvious one in terms of optimisation based on the logic that the more code we explore the more likely we are to see something go wrong. Our program uses these style of tests to ‘hunt’ for some more obscure mistakes which could be hidden deep within the code. We also run some more generic tests which don’t utilise this coverage based optimisation in order to test at a faster rate (since we don’t need to measure coverage etc), some more simple cases. Time is split between these cases, but multithreading allows us to do both effectively. As such it was a useful addition to provide a very different approach to fuzzing as compared to more standard approaches.

Finally, our something awesome also opens up many opportunities on how we can assign scores to each input to help scipy along the way. Our fuzzer would continue to work perfectly if we instead decided to measure something other than coverage
We think that our fuzzer using scipy to guide mutation changes is very weird and interesting. It opens up a lot of problems about how to convert vectors of floats into a usable format for our mutation strategies. 
