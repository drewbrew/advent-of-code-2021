def decompile(instructions: list[str]) -> str:
    result = []
    result.append("def step_1(next_digit: int) -> tuple[int, int, int, int]:")
    indent = "    "
    result += [f"{indent}{char} = 0" for char in "wxyz"]
    inputs_seen = 0
    for index, line in enumerate(instructions):
        if line.startswith("inp"):
            inputs_seen += 1
            if index:
                result.append(f"{indent}return w, x, y, z")
                result.append("")
                result.append("")
                result.append(
                    f"def step_{inputs_seen}(w: int, x: int, y: int, z: int, next_digit: int) -> tuple[int, int, int, int]:"
                )
            result.append(indent + "w = next_digit")
        else:
            words = line.split()
            instr = words[0]
            dest = words[1]
            assert dest in "wxyz"
            operand = words[2]
            if operand not in "wxyz":
                # force an error if it's not a valid int
                int(operand)
            if instr == "eql":
                result.append(f"{indent}{dest} = int({dest} == {operand})")
            else:
                operator = {"mul": "*=", "add": "+=", "div": "//=", "mod": "%=",}[instr]
                if instr == "mod":
                    result.append(f"{indent}assert {dest} >= 0")
                    result.append(f"{indent}assert {operand} > 0")
                elif instr == "div":
                    result.append(f"{indent}assert {operand} != 0")
                result.append(f"{indent}{dest} {operator} {operand}")
    result.append(f"{indent}return w, x, y, z")
    return "\n".join(result)


with open("day24.txt") as infile:
    print(decompile([line.strip() for line in infile]))
