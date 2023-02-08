DragonsRCool Language Guide
____________________________________________________________________________________________________________________________________________________________________________________
Functions which are called Program:

Always start with dragon, then function name, the parameters, the word fire, the body of the function, the word extinguish, and either add another function or the word end which kills the program. The first function in the progarm is always the one that starts the program.

dragon name param1, param2 fire
< body >
extinguish
end

____________________________________________________________________________________________________________________________________________________________________________________
The body:

Consist of commands which are all written like "<" command ">". A command can consist of a lot of things such as reading, writing, loops, conditions, variables, and function calls.
< body >

____________________________________________________________________________________________________________________________________________________________________________________
Creating a variable:

Starts with the scope either "big" or "small". Small meaning local and big mean global. Then the id. If it is a array you will use Parenthesis like this "()". You can then
also assign the variable with ":" and then do any expression or you can set it to a function. It will always end with a "$". Reassigning the variable is simple. You have the id,
and then the ":" sign. Then you can either set it to an expression or call a function. End it with a "$".

Declaring regular variable:
< big varName : expr $ >

Assigning declared variable to new expression:

< var : expr $ >

Array:
< small varName (size) :  expr  $
____________________________________________________________________________________________________________________________________________________________________________________
Printing a variable which is called a write in the BNF:

Start with the word "shoot" and follow this by a list of either id's, numbers, or string. The list is seperated by commas.

< shoot x, y z >

____________________________________________________________________________________________________________________________________________________________________________________
Reading a variable which is called read in the BNF:

Start with the word consume. This is then followed by an id which will be what stores the input. There is no check in read in so user must enter the correct type.

< consume x >

____________________________________________________________________________________________________________________________________________________________________________________
Loop which is equivelant to a while loop:

Start with the word "burn" Then you have a condition. The condition include a form of & and or (This information is listed in the condition section of the manual). This is followed by the word "<fire>". Then you have the body of the loop which works normally. Then to end the loop use the word "<extinguish>".

< burn expr condition expr fire < body > extinguish >

____________________________________________________________________________________________________________________________________________________________________________________
Path which which is equivelant to an if statement:

Start with the word "path", then a condition. Then the word "<here>", the body, and then "<here>"

Else statement:

Continue form your if statement and add the word "<there>", then the body, and end it with the word "<there>"

< path expr condition expr here
< body >
here
there
< body > 
there >

____________________________________________________________________________________________________________________________________________________________________________________
Arrays:

Work exacly like most arrays in languages. Use () with a number inside like arr(10) to reference index. Parenthesis always go after the id. Arrays index start at 0.

< arr (3) : 2 $>

____________________________________________________________________________________________________________________________________________________________________________________
conditions:

work like they do in most languages but instead of <, >, and = we use words

Key:
= : is
< : eats
<= : eats_more
> : spits
>= : spits_more

Conditions also include & and or:

Key:
& : also
or : either

____________________________________________________________________________________________________________________________________________________________________________________
Calling functions:

Start with the word hatch. Then the id of the function. Then either and empty [] or a list of ids, numbers, and strings inside of [] seperated by commas.

< hatch [paramList] >

____________________________________________________________________________________________________________________________________________________________________________________
Math:

Language include +, -, /, and *. Parenthesis to indicate order of expression are replaced with "{" and "}". ^ is used for the power sign

< x : {2 + 3 } * 2 ^ 2 >

____________________________________________________________________________________________________________________________________________________________________________________
Types:

Consist of String and Numbers. String are denoted by quotes and inside contain characters. Numbers can either have decimal places or not have decimal places. If a variable is not assigned when declared it will be type of None. Works similar to python.

< str : "Hello" $>
< num: 2 $>
____________________________________________________________________________________________________________________________________________________________________________________
Returning from a function:

A function does not have to declare what it is returning. Just set a variable equal to an expression when it is called.

< return expr >

____________________________________________________________________________________________________________________________________________________________________________________
How to run a created dragonsRCool program:

The program should be written in a text file. after that the program can be ran by typing in the terminal the following:

python dragonsRCool.py fileName
