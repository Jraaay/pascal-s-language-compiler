from compiler import Parser
from compiler import CodeGenerator
import os
import json
import sanic

app = sanic.Sanic(__name__)


def main_test():
    # parser = Parser.Parser(debug=True)
    # generator = CodeGenerator.CodeGenerator()
    # with open("./test/generator_test.pas") as f:
    #     ans = parser.parse(f.read())
    #     del(ans["ast_prod"])
    # with open("./test/generator_test.out", "w") as f:
    #     json.dump(ans, f, indent=4)
    parser = Parser.Parser(debug=True)
    generator = CodeGenerator.CodeGenerator()
    test_file_list = os.listdir("./test")
    for test_file in test_file_list:
        if test_file.endswith(".pas"):
            test_file_path = os.path.join("./test", test_file)
            ans = {}
            with open(test_file_path, "r") as f:
                ans = parser.parse(f.read())
            with open(test_file_path.replace(".pas", ".out"), "w") as f:
                json.dump(ans, f, indent=4)
            ans["code"] = generator.code_generate(
                ans["ast"], ans["symbolTable"])
            with open(test_file_path.replace(".pas", ".c"), "w") as f:
                f.write(ans["code"])
    dirs = os.listdir("./test")
    for dir in dirs:
        if os.path.isdir(os.path.join("./test", dir)):
            test_file_list = os.listdir(os.path.join("./test", dir))
            for test_file in test_file_list:
                if test_file.endswith(".pas"):
                    test_file_path = os.path.join("./test", dir, test_file)
                    ans = {}
                    with open(test_file_path, "r") as f:
                        ans = parser.parse(f.read())
                    ans["code"] = generator.code_generate(
                        ans["ast"], ans["symbolTable"])
                    with open(test_file_path.replace(".pas", ".out"), "w") as f:
                        json.dump(ans, f, indent=4)


@app.route("/api", methods=["POST"])
async def pascal2c(request):
    code = request.body.decode("utf-8")
    code = code.replace("\r\n", "\n")
    if code is None:
        return sanic.response.json({"error": "No code provided"})
    ans = app.config['parser'].parse(code)
    ans["code"] = app.config['generator'].code_generate(
        ans["ast"], ans["symbolTable"])
    return sanic.response.json(ans)


if __name__ == "__main__":
    main_test()
    parser = Parser.Parser(debug=False)
    app.config['parser'] = parser
    generator = CodeGenerator.CodeGenerator()
    app.config['generator'] = generator
    app.run()
