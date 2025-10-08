from lexical_parser import tokenize, Parser
from pprint import pprint


# Utility function to run and print test results
def run_test_case(description, code):
    print("=" * 60)
    print(f" Test: {description}")
    print("-" * 60)
    print("Code Input:")
    print(code)
    print("-" * 60)
    try:
        tokens = tokenize(code)
        print("Tokens:")
        pprint(tokens)
        parser = Parser(tokens)
        tree = parser.parse_program()
        print("\n Parse Tree:")
        pprint(tree)
    except (SyntaxError, RuntimeError) as e:
        print(f" Error: {e}")
    print("\n")


# expect pass test cases

# 1. Simple declaration
run_test_case("Single declaration with number set",
              """
let list = [5, 8, 12];
""")

# 2. Basic for loop with addition
run_test_case("For loop with addition inside",
              """
let list = [5, 8, 12];
for item in [5, 8, 12]:
    total = total + item;
    count = count + 1;
return total / count
""")

# 3. Minimal for loop (1 element list)
run_test_case("Single element list in for loop",
              """
let list = [10];
for item in [10]:
    total = total + item;
    count = count + 1;
return total / count
""")

# 4. Addition chain
run_test_case("Addition expression with multiple +",
              """
total = a + b + c;
""")

# 5. Missing semicolon
run_test_case("Missing semicolon after declaration",
              """
let list = [5, 8, 12]
""")

# expect fail test cases

# 6. Declaration followed by return THIS WILL FAIL BECAUSE OF THE STRICT GRAMMAR WE DEFINED IN OUR BNF
run_test_case("Declaration followed by simple return",
              """
let total = 10;
let count = 2;
return total / count
""")

# 7. Missing closing bracket
run_test_case("Missing closing bracket",
              """
let list = [5, 8, 12;
""")

# 8. Wrong keyword spelling
run_test_case("Incorrect keyword spelling",
              """
lset list = [5, 8];
""")

# 9. Invalid character
run_test_case("Unexpected symbol in code",
              """
let list = [5, 8, # 12];
""")

# 10. Missing return operands
run_test_case("Return missing right-hand operand",
              """
return total /
""")

# 11. For loop missing colon
run_test_case("Missing colon in for loop",
              """
let list = [5, 8, 12];
for item in [5, 8, 12]
    total = total + item;
    count = count + 1;
return total / count
""")

# 12. Extra tokens after program end
run_test_case("Extra token after program end",
              """
let list = [5, 8, 12];
return total / count
extra
""")

# edge cases

# 13. Empty list
run_test_case("Empty list declaration",
              """
let list = [];
""")

# 14. Whitespaces and tabs
run_test_case("Code with extra spaces and tabs",
              """
   let    list =    [5 , 8 , 12 ]   ;
   return   total   /   count
""")

# 15. Only return statement
run_test_case("Return statement alone",
              """
return total / count
""")
