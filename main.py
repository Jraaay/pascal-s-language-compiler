from compiler import Parser
import os
import json

def main():
    parser = Parser.Parser(debug=True)
    test_file_list = os.listdir("./test")
    for test_file in test_file_list:
        if test_file.endswith(".pas"):
            test_file_path = os.path.join("./test", test_file)
            ans = ''
            with open(test_file_path, "r") as f:
                ans = parser.parse(f.read())
            with open(test_file_path.replace(".pas", ".out"), "w") as f:
                json.dump(ans, f, indent=4)
    dirs = os.listdir("./test")
    for dir in dirs:
        if os.path.isdir(os.path.join("./test", dir)):
            test_file_list = os.listdir(os.path.join("./test", dir))
            for test_file in test_file_list:
                if test_file.endswith(".pas"):
                    test_file_path = os.path.join("./test", dir, test_file)
                    ans = ''
                    with open(test_file_path, "r") as f:
                        ans = parser.parse(f.read())
                    with open(test_file_path.replace(".pas", ".out"), "w") as f:
                        json.dump(ans, f, indent=4)

if __name__ == "__main__":
    main()