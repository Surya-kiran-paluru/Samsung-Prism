#include <bits/stdc++.h>
using namespace std;

void func_1();

float func_test_3(int arg,int argv[]);
int func_2(){
    cout<<"failed"<<endl;
    return 1;
}

int main(){
    cout<<"success"<<endl;
    func_2();
    cout<<"failed"<<endl;
    func_1();
    cout<<"success"<<endl;
    return 0;}

void func_1()
{
    cout<<"failed"<<endl;
}

float func_test_3(int arg,int argv[]){
    return 1.1;
}