from functions.write_file import write_file


def main():

    test_cases: list[list[str]] = [
        ["lorem.txt", "wait, this isn't lorem ipsum"],
        ["pkg/morelorem.txt", "lorem ipsum dolor sit amet"],
        ["/tmp/temp.txt", "this should not be allowed"],
    ]
    for case in test_cases:
        print(write_file("calculator", case[0], case[1]))


if __name__ == "__main__":
    main()
