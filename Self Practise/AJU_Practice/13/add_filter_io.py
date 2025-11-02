import sys

def main():
    for line in sys.stdin:
        line=line.strip()

        try:
            a, b=map(int, line.split())
            print(a+b)
        except:
            print("Invalid input", file=sys.stderr)
        sys.stdout.flush()
        
if __name__=="__main__":
    main()
