from functions.get_file_content import get_file_content


def main():

    result = get_file_content("calculator", "lorem.txt")
    print(f"lorem.txt length: {len(result)}")
    print(f"lorem.txt truncated: {'truncated' in result}")

    test_cases: list[str] = [
        "main.py",
        "pkg/calculator.py",
        "/bin/cat",
        "pkg/does_not_exist.py",
    ]
    for case in test_cases:
        if case == ".":
            print("Result for current directory:")
        else:
            print(f"Result for '{case}' directory:")
        print(get_file_content("calculator", case))


if __name__ == "__main__":
    main()
