#include <iostream>
using namespace std;

int main(){
    int i,j,k,n,suma, for_i, for_j, for_k;
    for_i = 0;
    for_j = 0;
    for_k = 0;
    cout<<"Entre el valor de n: ";
    cin>>n;
    suma = 0;
    for(i=1;i<=n;i=i*2){
        for(j=1;j<=n;j++){
            for(k=1;k<=n;k++){
                suma = suma + 1;
                for_k++;
            }
            for_j++;
        }
        for_i++;
    }
    cout<<"La suma es: "<<suma<<endl;
    cout<<"i:"<<for_i<<" j: "<<for_j<<" k: "<<for_k<<endl;
    system("pause");
}