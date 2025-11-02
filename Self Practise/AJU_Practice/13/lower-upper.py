import subprocess
import sys
sys.stdout.flush()

def main():

    process=subprocess.Popen(
            ["tr", "A-Z", "a-z"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
    )
    
    try:
        while True:
            line=input("prompt> ")
            if not line:
                break

            # Send line to filter process
            process.stdin.write(line + "\n")
            process.stdin.flush()

            # Read transformed output
            output = process.stdout.readline()
            print(output, end="")
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass 
    finally:
        process.stdin.close()
        process.wait()

if __name__=="__main__":
    main()
