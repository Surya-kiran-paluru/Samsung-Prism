#include <iostream>
#include "test\Nothing.h"
using namespace std;

int main(){

    bool flag_application = Nothing::open_application();

    if(flag_application){
        cout<<"\nHello Message"<<endl;
        try{
            bool i = Nothing::open_camera();
            if(!i){
                throw 'a';
            }
        }
        catch(char a){
            cout<<"Error in opening camera"<<endl;
        }
        
    }

    else{
        cout<<"Failed to open application"<<endl;
    }

    return 0;

}