# AltWalker_fragmentation_example
An example how to use AltWalker to generate tests for de-fragmentation code. Includes installation instructions and tips. 

The instructions are for installation and execution on WSL (Windows Subsystem for Linux). It probably works well on any Linux installation, but I only worked with it on WSL with Ubuntu 20.04 distribution. 

Installation and resources
1)	For Window users: Install WSL:  
Instructions:  https://docs.microsoft.com/en-us/windows/wsl/install-manual . 
 Note that if you have a backup system running on your Windows machine, it will most likely NOT backup the WSL installation. So consider how to save your development files (maybe use Git or similar), so you don’t lose everything when (not “if”) your disk crashes. 
 Note also that the WSL takes disk space, but does not give back the space after you delete files in it. So the installation can grow to be quite large (10s or more GBytes). See this URL how to shrink the installation: https://stephenreescarter.net/how-to-shrink-a-wsl2-virtual-disk/ 
2)	AltWalker installation instructions: https://gitlab.com/altom/AltWalker/AltWalker . Note that this example was developed and tested on WSL, with Ubuntu 20.04 distribution. 

3)	AltWalker documentation: https://altom.gitlab.io/AltWalker/AltWalker/index.html

4)	AltWalker is a python wrapper for GraphWalker. See  documentation for GraphWalker here: https://github.com/GraphWalker/graphwalker-project/wiki . I found of special important the page that explains the stop conditions:  https://github.com/GraphWalker/graphwalker-project/wiki/Generators-and-stop-conditions  .

5)	GraphWalker Google group:  https://groups.google.com/g/graphwalker. It is active (at least was when I wrote this…)

Running the example
1)	In case you made any changes to the model, you can check it for errors using: 

      altwalker check -m models/fragmentation_model.json "random(vertex_coverage(100))"

A good model will give this result: 

      Checking models syntax:

        * models/fragmentation_model.json::Fragment_factory [PASSED]

      Checking models against stop conditions:

        No issues found with the model(s).
 

2)	To run the model, use a command similar to this one (you may want to change the stop criteria; see https://github.com/GraphWalker/graphwalker-project/wiki/Generators-and-stop-conditions )

      altwalker online tests -m models/fragmentation_model.json "random(time_duration(2))"

Besides the output to screen, this will create a text file “fragments.txt” with description of fragments (size, fragment number). This file can be used to create actual tests (translate the fragments information into packets which are sent to the de-fragment code, to see it manages to build the sent message correctly). 
Note: Just in case anyone thinks of using this example for testing de-fragmentation (unlikely, I know): Don’t send the same information in each fragment, since you won’t be able to note a bug where fragments were assembled not in order. 

3)	The example given is for positive tests: it describes valid fragments and correct setting of fragment numbers. You can modify this model to create more interesting tests. For example: Create fragments that are out-of-order. See file test-non_seq_fragNumbers.py 

4)	Negative tests can be created by modifying the code to (for example) skip a fragment. Or send the same fragment twice. You can also add illegal transitions to the state machine, and take them only sometimes (there is a “weight” parameter for each edge, that can be added to the edge description in the model json file).


