def transcribeArgs(rawArgument):
        done = False
        while not done:
            if "~" in rawArgument:
                rawArgument = rawArgument.replace("~", " not ")
            elif "&" in rawArgument:
                rawArgument = rawArgument.replace("&", " and ")
            elif "v" in rawArgument:
                rawArgument = rawArgument.replace("v", " or ")
            elif "<>" in rawArgument:
                operatorIndex = rawArgument.index("<>")
                rawArgument = "({} and {}) or (not {} and not {})".format(rawArgument[:operatorIndex], rawArgument[(operatorIndex + 2):], rawArgument[:operatorIndex], rawArgument[(operatorIndex + 2):])
            elif ">" in rawArgument:
                operatorIndex = rawArgument.index(">")
                rawArgument = "not " + rawArgument[:operatorIndex] + " or " + rawArgument[(operatorIndex + 1):]
            else:
                done = True
        return rawArgument
    
#takes a string and returns the max (or least) depth of nested parentheses
def maxParenthesesDepth(string, maxOrLeast = 'max'):
    #accumulator variables
    max = 0
    least = 0
    currentCount = 0
    #parses each character
    for character in string:
        #will make 'max' the highest value reached
        if currentCount > max:
            max = currentCount
        #will make 'least' the lowest value reached
        elif currentCount < least:
            least = currentCount
        #tracks where the current depth is at
        currentCount += parenthesesCheck(character)
    #determines what will be returned
    if maxOrLeast == "max":
        return max
    elif maxOrLeast == 'least':
        return least
        
    
        
#takes a proposition and translates it into a logically equivelent
#proposition using pythonic operators
def simplifyCompound(premise):
    #makes copy for manipulation purposes, to save original for reference
    alteredPremise = premise
    
    #checks if there are any parentheses
    if "(" in alteredPremise:
        #establishes a degree of nested parentheses depth (for priority translation)
        maxDegree = maxParenthesesDepth(alteredPremise)
        #variable for current degree being translated
        depthDegree = maxDegree
        #parsing variables
        parenthesesCount = 0
        indexCount = 0
        #temporary string for holding stages of transcription
        tempString = ''
        #loop for translating the contents of parentheses
        while depthDegree > 0:
            #checks that the index is within the character limit 
            if indexCount < len(alteredPremise):
                parenthesesCount += parenthesesCheck(alteredPremise[indexCount])
                #if the parentheses has reached the goal depth, translation sequence initiates
                if (parenthesesCount == depthDegree):
                    #takes the string slice of everything after the triggered parenthesis 
                    tempstring = alteredPremise[(indexCount + 1):]
                    
                    #variable to stand in for the triggered parenthesis
                    tempCount = 1
                    #loops/parses until reaches a point where the corrolated terminal parenthesis is reached
                    while tempCount != 0:
                        for index in range(len(tempstring)):
                            tempCount += parenthesesCheck(tempstring[index])
                            #once hits the terminal parenthesis...
                            if tempCount == 0:
                                #...shortens substring to exclude everything after terminal parenthesis
                                tempstring = tempstring[:index]
                                break
                    #rewrites the alteredPremise to contain the the transcribed isolated substring,
                    #replacing the previous substring.
                    alteredPremise = alteredPremise[0:indexCount+1] + transcribeArgs(tempstring) + alteredPremise[(indexCount + index + 1):]
                    #corrects the parsing index to skip to after the newly tranlated segment
                    indexCount += len(transcribeArgs(tempstring))
                #moves the index to parse the next character
                indexCount += 1
            #once has parsed entire string, changes the parenthetical depth that needs to be checked
            #and sets index to 0 to reset parsing
            else:
                depthDegree -= 1
                indexCount = 0
                
        #translates the string as a whole
        alteredPremise = transcribeArgs(alteredPremise)        
        return alteredPremise
    
    #translates whole proposition string
    else:
        return transcribeArgs(premise)
    
        
#takes all the propositions, finds the atomic statement variables,
    #and aggregates and returns a list of those variables
def atomicStatementFinder(premiseList,conclusion=""):
    listOfAtomics = []
    for premise in premiseList:
        for character in premise:
            #if character is an uppercase letter...
            if (ord(character) >= 65) and (ord(character) <= 90):
                #...and is not already on the list...
                if character not in listOfAtomics:
                    #...it will be added to the list.
                    listOfAtomics.append(character)
    #same steps for conclusion
    for character in conclusion:
        if (ord(character) >= 65) and (ord(character) <= 90):
            if character not in listOfAtomics:
                listOfAtomics.append(character)
    return listOfAtomics
    
    
def parenthesesCheck(singleCharacter):
    if singleCharacter == "(":
        return 1
    elif singleCharacter == ")":
        return -1
    else:
        return 0


def indexCorrect(segment):
    return len(transcribeArgs(segment)) - len(segment)



def truthValueGenerator(listVars):
    truthArray = []
    for var in range(len(listVars)):  
        truthValues = ( ('True.' * (2**var)) + ('False.' * (2**var)) ) * (2 ** (len(listVars)-(var + 1)))
        truthValues = truthValues.split('.')
        truthArray.append(truthValues)
    return truthArray


def rowEvaluator(statements, variables, truthValues):
    copyStatements = statements[:]
    validityCondition = ""
    #change each statment variable into a would-be-Boolean string
    for statement in range(len(copyStatements)):       
        for variable in variables:
            if variable not in ['F','T']:
                copyStatements[statement] = copyStatements[statement].replace(variable, truthValues[variables.index(variable)])
        #Change the 'T' to True, manually 
        if 'T' in variables:
            characterCount = 0
            #will stop once reaches the end of the string
            while characterCount < len(copyStatements[statement]):
                #check if it's already in boolean form
                if  copyStatements[statement][characterCount] == 'T' and copyStatements[statement][characterCount+1] != 'r':
                    copyStatements[statement] = copyStatements[statement][:characterCount]+ "True" + copyStatements[statement][characterCount + 1:]
                    #update the index marker to account for new letters introduced
                    characterCount += 3
                characterCount += 1
        #Change the 'F' to False, manually    
        if 'F' in variables:
            characterCount = 0
            #will stop once reaches the end of the string
            while characterCount < len(copyStatements[statement]):
                #check if it's already in boolean form
                if  copyStatements[statement][characterCount] == 'F' and copyStatements[statement][characterCount+1] != 'a':
                    copyStatements[statement] = copyStatements[statement][:characterCount]+ "False" + copyStatements[statement][characterCount + 1:]
                    #update the index marker to account for new letters introduced
                    characterCount += 4
                characterCount += 1
                
        #evaluates string as code to produce a Boolean
        copyStatements[statement] = eval(copyStatements[statement])
        
        #strings all the boolean results of each statement
        #together to reevaluate if ALL are jointly true
        if statement <= len(copyStatements) - 2:
            validityCondition =  validityCondition + str(copyStatements[statement]) + " "
            if statement < len(copyStatements) - 2:
                validityCondition =  validityCondition + "and "
    if len(copyStatements) == 1:
        validityCondition = str(copyStatements)
    #evaluates the premises together to ensure all are true
    #so they are able to prove an invalidity
    validityCondition = eval(validityCondition)
    #if all premises true and conclusion false
    if validityCondition and not copyStatements[-1]:
        return "invalid"
    #else continues trying until finds a proof of invalidity 
    #or proves by validity by absense of the former
    else:
        return 'pass'
    
    
# takes an input premise and outputs None for bad format, and does
def premiseInput(premise):
    #check for character content
    if len(premise) == 0:
        print("Empty propositions are not allowed")
        return None
    #sets variable to check for symmetrical sets of parentheses
    evenParentheses = 0
    for symbol in premise:
        #checks if character is not an uppercase letter
        if not ((ord(symbol) >= 65) and (ord(symbol) <= 90)):
            #checks to see if character is not a legal character/operator in this program
            if symbol not in ['&', 'v', '>', '<', '~', '(', ')', ' ']:
                #if is not of either category, character is not legal.
                print("Please input only uppercase letters and the operators listed previously.")
                return None
        #uses function to track parenthetical symmetry
        evenParentheses += parenthesesCheck(symbol)
    #checks if there is incorrect parenthetical ordering or symmetry
    if (maxParenthesesDepth(premise, 'least') != 0) or (evenParentheses != 0):
        print("Please check your parentheses are being used correctly.")
        return None
    
    #simulates program to see if causes a syntax error when evaluated
    #defines variables
    premiseVars = atomicStatementFinder(premise)
    #puts into usable format for later functions
    tempPremise = [simplifyCompound(premise)]
    #checks if execution of the premise into program will produce a syntax error
    try:
        previewResult = majorEvaluator(premiseVars, tempPremise)
        return True
    except SyntaxError:
        print('Incorrect Syntax: Please ensure there are no consecutive variables or consecutive operators.')
        return None



def majorEvaluator(variableList, listPremises, conclusion = ''): #will replace all instances of variables into booleans
    allTruthValues = truthValueGenerator(variableList)
    if conclusion != '':
        allStatements = listPremises + [conclusion]
    else:
        allStatements = listPremises
    for assignRow in range(2**len(variableList)):
        groupAssignment = []
        for variable in range(len(variableList)):
        ##need to assign the throw the row of truth values assignments into the string swap function (with vars list)
            groupAssignment.append(allTruthValues[variable][assignRow])
        if rowEvaluator(allStatements, variableList, groupAssignment) == 'invalid':
            return 'invalid'
    return 'valid'



def documentPremise(premises, conclusion, result):
    translationDoc = open('validityResults.txt', 'w')
    translationDoc.write('\n------------------------------\nValidity Validator Results\n------------------------------\n')
    for proposition in range(len(premises)+1):
        if proposition == len(premises):
            translationDoc.write('THEREFORE:\n{}. {}\n'.format(proposition + 1, conclusion))
        else:
            translationDoc.write('{}. {}\n'.format(proposition + 1, premises[proposition]))
    translationDoc.write('\n This argument is...{}!'.format(result.upper()))


    translationDoc.close()

    translationDoc = open('validityResults.txt', 'r')
    print(translationDoc.read())
    translationDoc.close()

#will display examples of possible inputs and outputs for user, if opt in
def example():
    #prompt decision for optional example
    acceptExample = input('Before we begin, would you like to see an example input?(y/n): ')
    if acceptExample.lower() == "y":
        print('1. A')
        print('2. A > B')
        print('3. C   (Conclusion)')
        print("This argument is ... INVALID!")
        acceptExample = input('\nWould you like to see a more complex example?(y/n): ')
        #prompts for another example
        if acceptExample.lower() == 'y':
            print('1. (S v T) <> ~E')
            print('2. S > (F & ~G)')
            print('3. A > W')
            print('4. T > ~W')
            print('5. (~E & A) > ~G   (Conclusion)')
            print("This argument is ... VALID!")
            print("\nLet's begin!")
##  printouts for anything but an input of 'y'
        else:
            print("I'll take that as excitement to begin!")
    else:
            print("I'll take that as excitement to begin!")

#triggers all functions to execute the program
def main():
    print('''    INTRUCTIONS
-------------------
This is the Validity Validator!
This will tell you if a given symbolic argument is logically valid or not, according to FORMAL LOGIC.

DISCLAIMER: Validity ONLY means that the conclusion cannot be false while the premises are true.
Validity does not mean the conclusion is true, that it's absence means the conclusion is false,
nor that an argument is good.
("I'm a student and not a student. Therefore, I'm a king." is valid)
("I'm a student. I am in a computer science class. Therefore, I am in CSCI 141" is invalid)

When typing the premises/conclusion, use the following symbols for your logical operators and operands:
        AND = '&'
        OR = 'v' (lowercase only please)
        Conditional (if,then) = '>'
        Bi-Conditional (if and only if) = '<>'
        NOT = '~'
        Variables = Use only capital letters for atomic statements
        Parentheses - Use () to separate smaller logical components
        ''')
    
    #optional example
    example()
    #ensures that user puts in correct integer input
    while True:
        try:
            numPremises  = int(input("\nHow many premises in the argument?: "))
            if numPremises > 0:
                break
            else:
                print("\nPlease enter positive integers only\n")
        #if user inputs non-integer, will not produce error
        except ValueError:
            print("\nPlease enter positive integers only")
            continue
    #establishes list for original premise inputs to be saved
    originalPremises = []
    #prompts the user for a premise based on previous input
    for p in range(0,numPremises):
        #won't stop looping until correct premise format is input
        while True:
            tempStatement = (input("Write in Premise #{}: ".format(p+1)))
            #uses custom function to verify format
            if premiseInput(tempStatement) != None:
                #if in proper format, appends to premise list
                originalPremises.append(tempStatement)
                break
            
    #loops until correctly formatted conclusion is input                    
    while True:    
        originalConclusion = input("Enter the conclusion: ")
        #checks the formatting of the input
        if premiseInput(originalConclusion) != None:
            break
    
    #makes copies of premises/conclusion for manipulation
    premises = originalPremises[:]
    conclusion = originalConclusion
    
    #creates a list of all variables used in propositions
    atomicList = atomicStatementFinder(premises, conclusion)
    
    #tranlates each proposition to be used for later evaluation
    for statement in premises:
        premises[premises.index(statement)] = simplifyCompound(statement)
    conclusion = simplifyCompound(conclusion)
    
    #function will evaluate to either 'valid' or 'invalid'
    overallResult = majorEvaluator(atomicList, premises, conclusion)
    
    #writes and prints the results
    documentPremise(originalPremises,originalConclusion,overallResult)


#triggers the program to begin
main()