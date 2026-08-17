from functions.get_files_info import get_files_info

def main():
    # print(get_files_info("calculator", "."))
    # print(get_files_info("calculator", "/bin"))
    # print(get_files_info("calculator", "../"))
    # print(get_files_info("calculator", "main.py"))

    test_cases: list[str] = [".", "pkg", "/bin", "../"]
    for case in test_cases:
        if case == ".":
            print("Result for current directory:")
        else:
            print(f"Result for '{case}' directory:")
        print(get_files_info("calculator", case))

if __name__ == "__main__":
    main()
