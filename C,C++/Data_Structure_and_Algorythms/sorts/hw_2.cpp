#include <iostream>
using namespace std;

int power(int);
int power2(int);

int main(){
    int n,potencia;
    cout<<"Digite una entrada para n: ";
    cin>>n;
    potencia = power(n);
    cout<<potencia<<endl;
    system("pause");
}
int power2(int n){
    if (n<=0){
        return 1;
    }
    else{
        return  2*power2(n-1);
    }
}
int power(int n){
    if (n<=0){
        return 1;
    }
    else{
        return power(n-1)+power(n-1);
    }
}
