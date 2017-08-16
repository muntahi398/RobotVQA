# RobotVQA

   Robohow is the European Research Project that aims at enabling robots to competently perform human-scale daily manipulation activities such as cooking in an ordinary kitchen. However, to complete such tasks, robots should not only exhibit standard visual perception capabilities such as captioning, detection, localization or recognition, but also demonstrate some cognitive vision, in which all these capabilities including considerable reasoning are integrated together, so that semantically deep understanding of the unstructured and dynamic scene can be reached. 
   In this thesis, we formulate the underlying general perception problem as the problem of Visual Question Answering, however with a strong focus on the subproblem of dense captioning referring to the open-ended question "what do you see?" and which is central in tackling general perception.Then, we address the VQA problem by implementing a Deep-Learning-based module, that initially segments the input image into meaningfull regions, encodes the question and the regions, then map them onto the same vector space. Following the projection, the system initializes an episodic memory with the question vector and progressively decode the question by selectively paying attention to the facts actually corresponding to the input image. Finally, the natural language generation of the answer followed by the computation of coordinates of regions of concern takes place. Unlike most of the existing solutions to the VQA problem, this module does not merely generate answers as natural language sentences, wich would still be untructured for the robot, but also care for their structure.
