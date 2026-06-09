def media(a , b, c):
    return (a + b + c) / 3

def main():
    a = int(input("1 Valor? "))
    b = int(input("2 Valor? "))
    c = int(input("3 Valor? "))
    print(f'A média é {media(a, b, c):.2f}')

if __name__ == '__main__':
    main()
