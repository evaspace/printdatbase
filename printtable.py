import sqlite3
import sys
from colorama import Fore, Style, init

init(autoreset=True)
ASCII_BANNER = f"""
{Fore.CYAN}
                                                                                
▗▄▄                 ▗▄▄▖                     ▗▄▄▖        █                      
▐▛▀█       ▐▌       ▐▛▀▜▌                    ▐▛▀▜▖       ▀        ▐▌            
▐▌ ▐▌ ▟██▖▐███  ▟██▖▐▌ ▐▌ ▟██▖▗▟██▖ ▟█▙      ▐▌ ▐▌ █▟█▌ ██  ▐▙██▖▐███  ▟█▙  █▟█▌
▐▌ ▐▌ ▘▄▟▌ ▐▌   ▘▄▟▌▐███  ▘▄▟▌▐▙▄▖▘▐▙▄▟▌     ▐██▛  █▘    █  ▐▛ ▐▌ ▐▌  ▐▛ ▜▌ █▘  
▐▌ ▐▌▗█▀▜▌ ▐▌  ▗█▀▜▌▐▌ ▐▌▗█▀▜▌ ▀▀█▖▐▛▀▀▘     ▐▌    █     █  ▐▌ ▐▌ ▐▌  ▐▌ ▐▌ █   
▐▙▄█ ▐▙▄█▌ ▐▙▄ ▐▙▄█▌▐▙▄▟▌▐▙▄█▌▐▄▄▟▌▝█▄▄▌     ▐▌    █   ▗▄█▄▖▐▌ ▐▌ ▐▙▄ ▝█▄█▘ █   
▝▀▀   ▀▀▝▘  ▀▀  ▀▀▝▘▝▀▀▀  ▀▀▝▘ ▀▀▀  ▝▀▀      ▝▘    ▀   ▝▀▀▀▘▝▘ ▝▘  ▀▀  ▝▀▘  ▀                                                                                
by Morgan PIERREFEU.
"""
def f(m):
    print(Fore.RED + f"\n[ERROR] {m}")
    sys.exit(1)

def p(v):
    if v is None:
        return f"{Fore.RED}NULL{Style.RESET_ALL}"
    if v == "":
        return f"{Fore.RED}EMPTY{Style.RESET_ALL}"
    if v == 0 or v == "0":
        return f"{Fore.YELLOW}0{Style.RESET_ALL}"
    return str(v)

def m():
    print(ASCII_BANNER)
    dn = input(Fore.GREEN + "Database file (e.g. data.db): ").strip()
    
    try:
        cn = sqlite3.connect(dn)
        cr = cn.cursor()
    except sqlite3.Error:
        f("Cannot open file. Check the name.")

    cr.execute("SELECT name FROM sqlite_master WHERE type='table'")
    ts = [r[0] for r in cr.fetchall()]
    
    if not ts:
        f("No tables found in this database.")

    print(Fore.YELLOW + "\nAvailable tables:")
    for i, t in enumerate(ts, 1):
        print(f"  {Fore.CYAN}{i}{Style.RESET_ALL} - {t}")

    try:
        ti = int(input(Fore.GREEN + "\nEnter table number: ")) - 1
        if ti < 0 or ti >= len(ts): raise ValueError
        tn = ts[ti]
    except ValueError:
        f("Invalid table number.")

    cr.execute(f"PRAGMA table_info({tn})")
    cs = [r[1] for r in cr.fetchall()]
    
    print(Fore.YELLOW + f"\nColumns in '{tn}':")
    for i, c in enumerate(cs, 1):
        print(f"  {Fore.CYAN}{i}{Style.RESET_ALL} - {c}")

    rc = input(Fore.GREEN + "\nColumns to show (e.g. 1,3) or ENTER for all: ").strip()
    try:
        if not rc:
            sc = cs
        else:
            ci = [int(x) - 1 for x in rc.split(",")]
            sc = [cs[i] for i in ci]
    except (ValueError, IndexError):
        f("Invalid column selection.")

    sn = input(Fore.GREEN + "Sort by column # (ENTER to skip): ").strip()
    oc = ""
    if sn:
        try:
            si = int(sn) - 1
            if 0 <= si < len(cs):
                sd = input(Fore.GREEN + "Order (a=asc, d=desc) [default: a]: ").lower()
                dr = "DESC" if sd.startswith('d') else "ASC"
                oc = f"ORDER BY {cs[si]} {dr}"
            else:
                print(Fore.RED + "Invalid sort column, skipping.")
        except ValueError:
            print(Fore.RED + "Invalid input, skipping.")

    l = input(Fore.GREEN + "Rows to display [default: 20]: ").strip()
    l = int(l) if l.isdigit() else 20

    q = f"SELECT {', '.join(sc)} FROM {tn} {oc} LIMIT ?"

    try:
        cr.execute(q, (l,))
        rs = cr.fetchall()
    except sqlite3.Error as e:
        f(f"Query error: {e}")

    if not rs:
        print(Fore.YELLOW + "\nTable is empty or query returned nothing.")
        return

    fr = [[p(c) for c in r] for r in rs]
    
    ws = [len(c) for c in sc]
    for r in fr:
        for i, c in enumerate(r):
            cl = len(c) - (len(Fore.RED) + len(Style.RESET_ALL)) if Fore.RED in c else len(c)
            cl = cl - (len(Fore.YELLOW) + len(Style.RESET_ALL)) if Fore.YELLOW in c else cl
            ws[i] = max(ws[i], cl)

    sp = "+".join("-" * (w + 2) for w in ws)
    print(Fore.BLUE + f"\n+{sp}+")
    
    h = "|".join(f" {Fore.MAGENTA}{c.ljust(ws[i])}{Style.RESET_ALL} " for i, c in enumerate(sc))
    print(f"|{h}|")
    print(Fore.BLUE + f"+{sp}+")

    for r in fr:
        ln = ""
        for i, c in enumerate(r):
            ansi_len = 0
            if '\033' in c:
                ansi_len = len(c) - (len(c) - (len(Fore.RED) + len(Style.RESET_ALL))) if Fore.RED in c else len(c) - (len(c) - (len(Fore.YELLOW) + len(Style.RESET_ALL)))
            
            pd = ws[i] + ansi_len
            ln += f" {c.ljust(pd)} |"
        print(f"|{ln[:-1]}|")

    print(Fore.BLUE + f"+{sp}+")
    print(Fore.CYAN + f"\nShowing {len(rs)} row(s).")
    cn.close()

if __name__ == "__main__":
    try:
        m()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\nUser interruption. Goodbye!")
        sys.exit(0)