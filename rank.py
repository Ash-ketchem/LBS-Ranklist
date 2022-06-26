import os
import pandas as pd
import sys


def utils(df, names):
    names = [i for i in names.split("-") if i]

    for name in names:
        print("\n[*] Searching data of ", name)
        res = df.loc[df.NAME == name.upper()]
        if all(res):
            for value in res.values:
                res = value
                print("[+] Results \n")
                print(f"Name : {res[0]}")
                print(f"Total Marks : {res[1]}")
                print(f"CS : {res[2]}")
                print(f"Maths : {res[3]}")
                print(f"Reasoning : {res[4]}")
                print(f"Rank : {res[5]}", "\n")
        else:
            print("[-] No data found, name might be incorrect")


def main():
    print(
        """
              ██████
            ▒██    ▒
            ░ ▓██▄
              ▒   ██▒
            ▒██████▒▒
            ▒ ▒▓▒ ▒ ░
            ░ ░▒  ░
            ░  ░  ░
                  ░
           """
    )

    if not os.path.exists("results.txt"):
        print("[-] results.txt file required")
        sys.exit()

    print("\n", "LBS RESULTS WITH RANK", "\n", len("LBS RESULTS WITH RANK") * "_", "\n")

    with open("results.txt", "r") as f:
        data = f.readlines()

    rank_list = []
    count = 1

    for line in data:
        contents = [
            int(i.split(".")[0]) if ".00" in i else i
            for i in [i for i in line.split(" ") if i]
        ]

        marks = [i for i in contents if type(i) is int]
        if len(marks):
            rank_list.append(
                {
                    "name": " ".join(i for i in contents[3:] if type(i) is str),
                    "mark": marks[0],
                    "cs": marks[1],
                    "maths": marks[2],
                    "aptitude": marks[3],
                }
            )

    rank_list = sorted(
        sorted(
            sorted(
                sorted(rank_list, key=lambda x: x["mark"], reverse=True),
                key=lambda x: (x["mark"], x["cs"]),
                reverse=True,
            ),
            key=lambda x: (x["mark"], x["cs"], x["maths"]),
            reverse=True,
        ),
        key=lambda x: (x["mark"], x["cs"], x["maths"], x["aptitude"]),
        reverse=True,
    )

    max_total_marks = max([i["mark"] for i in rank_list])
    max_cs_marks = max([i["cs"] for i in rank_list])
    max_maths_mark = max([i["maths"] for i in rank_list])
    max_apptitude_mark = max([i["aptitude"] for i in rank_list])

    for i, guy in enumerate(rank_list):
        rank_list[i]["Rank"] = count
        count += 1

    df = pd.DataFrame(rank_list)
    df.columns = [col.upper() for col in df.columns]

    print("[+] saving the results to results.csv\n")
    df.to_csv("results.csv", index=True)

    print("[+] First 15 Ranks\n")
    print(df.head(15), "\n")

    print("[*]Some additional information")
    print("[+] Maximum marks got in computer Science : ", max_cs_marks)
    print("[+] Maximum marks got in Mathematics and Statistics : ", max_maths_mark)
    print("[+] Maximum marks got in Logical Reasoning : ", max_apptitude_mark)

    targets = input(
        "\n[*] enter the name of the person/people you want to search for seperated with a hyphen(-): "
    )
    if targets:
        utils(df, targets)


if __name__ == "__main__":
    main()
