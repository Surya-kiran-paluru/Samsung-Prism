import imp_test
def func1():
    print('success')
    def func3():
        print("success")
        func1()
        print('failed')   
    if 5 < 2 :
        print("success")
        if 5 > 2:
            print("success")
    else:
        print("failed")
        if 5 > 2:
            print("success")

if __name__ == "__main__":
    print("success")
    func1()
    imp_test.func2()
    print("failed")
    
    