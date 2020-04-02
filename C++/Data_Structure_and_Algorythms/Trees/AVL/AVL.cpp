#include "iostream"
#include "conio.h"
#include "stdio.h"
using namespace std;

class nodoarbol
{ 
    public:
    int info,fb;
    nodoarbol *der,*izq;
    nodoarbol()
    {
    der=NULL;
    izq=NULL;
    } nodoarbol(int dato,int fb)
    {
    fb=fb;
    info=dato;
    izq=NULL;
    der=NULL;
    }
};
class AVL
{
    private:
        nodoarbol *raiz;
    public:
        AVL()
        {
            raiz=NULL;
        }   
        ~AVL()
        {
            cout<<"\nborrando..."<<endl;
            borrar_nodos(raiz);
            cout<<"borrado finalizado"<<endl;
            system("pause");
        } 
        void borrar_nodos(nodoarbol *raiz)
        {
            if(raiz != NULL)
            {
                borrar_nodos(raiz->izq);
                borrar_nodos(raiz->der);
                cout<<"Borro "<<raiz->info<<endl;
                delete raiz;
            }
        }
    void insertar()
    {
        nodoarbol *aux1,*aux2,*aux3;
        int salir;
        salir=0;//Variable que controla el ingreso de nodos repetidos
        aux1=new nodoarbol;
        aux2=raiz;
        aux3=NULL;
        cout<<"Ingrese el dato del nodo a insertar: ";
        cin>>aux1->info;
        evaluar_repetido(raiz,aux1->info,salir);
        if(salir!=1)
        {
            while(aux2!=NULL)
            {
                aux3=aux2;
                if(aux1->info>aux2->info)
                {
                aux2=aux2->der;
                }
                else
                {
                aux2=aux2->izq;
                }
            } 
            if(aux3==NULL)
            {
                raiz=aux1;
            }
            else
            {
                if(aux1->info<aux3->info)
                {
                    aux3->izq=aux1;
                }
                else
                { 
                    aux3->der=aux1;
                }
            }
            factor_de_balanceo(raiz); //Asigna el factor de balance
            //(fb) a cada nodo del arbol
            balancear(raiz);//Balancea el arbol
            factor_de_balanceo(raiz);//Asigna el fb a cada nodo
            // despues de balancear el arbol
        }
    } 
    void evaluar_repetido(nodoarbol *raiz,int valor,int &salir) //Recorrela //lista comparando el nodo ingresado con los demas del arbol.
    {
//si se encuentra un nodo que coincide, la variable salir se modifica.
        if(raiz!=NULL)
        {
            evaluar_repetido(raiz->izq,valor,salir);
            if(raiz->info==valor)
            {
                salir=1;
                cout<<"\nEl nodo ya existe\n"<<endl;
            } 
            else
            {
            evaluar_repetido(raiz->der,valor,salir);
            }
        }
    }
    void factor_de_balanceo(nodoarbol *raiz)//Determina el factorN de balance de cada nodo
        {
            if(raiz!=NULL)
            {
                int nivelizq,nivelder,diferencia;
                nivelizq=nivel(raiz->izq);
                nivelder=nivel(raiz->der);
                diferencia=nivelizq-nivelder;
                raiz->fb=diferencia;
                factor_de_balanceo(raiz->izq);
                factor_de_balanceo(raiz->der);
            }
        } 
        int nivel(nodoarbol *raiz)//Determina los niveles del arbol
            {
                if(raiz==NULL)
                {
                    return 0;
                }
                else
                {
                    int a,b;
                    a=nivel(raiz->izq);
                    b = nivel(raiz->der);
                
                    if (a<b)
                    {
                        return b+1;
                    }
                    else
                    {
                        return a+1;
                    }
                }
            }
        void balancear (nodoarbol *raiz)
        {
            if(raiz!=NULL)
            {
                //nodoarbol *apunt;
                //nodoarbol *temp;
                //int aux;
                balancear(raiz->izq);
                balancear(raiz->der);
                if(raiz->fb==(-2))
                {
                    if(raiz->der->fb==-1)
                    {
                    rotar_izq(raiz);
                    } 
                    else
                    {
                        if(raiz->der->fb==1)
                        {
                            // doble rotacion
                            rotar_der(raiz->der);
                            rotar_izq(raiz);
                        } 
                        else
                        {
                            if(raiz->der->fb==0)
                            {
                                rotar_izq(raiz);
                            }
                        }
                    }
                }
                if(raiz->fb==2)
                {
                    if(raiz->izq->fb==1)
                    {
                        rotar_der(raiz);
                    } 
                    else
                    {
                        if(raiz->izq->fb==-1)
                        {
                            rotar_izq(raiz->izq);
                            rotar_der(raiz);
                        }
                        else
                        {
                            if(raiz->izq->fb==0)
                            {
                                rotar_der(raiz);
                            }
                        }
                    }
                }
            }
        } 
        nodoarbol *devolver_raiz()
        {
            return raiz;
        }
        void rotar_izq(nodoarbol *raiz)
            {
                int aux;
                nodoarbol *apunt;
                apunt=raiz->der;
                aux=raiz->info;
                raiz->der=apunt->der;
                apunt->der=apunt->izq;
                apunt->izq=raiz->izq;
                raiz->izq=apunt;
                raiz->info=apunt->info;
                apunt->info=aux;
            }
        void rotar_der(nodoarbol *raiz)
            {
                int aux;
                nodoarbol *apunt;
                apunt=raiz->izq;
                aux=raiz->info;
                raiz->izq=apunt->izq;
                apunt->izq=apunt->der;
                apunt->der=raiz->der;
                raiz->der=apunt;
                raiz->info=apunt->info;
                apunt->info=aux;
            }
// DESPLIEGA EL ARBOL USANDO INORDEN - INCLUYE fb
        void despliega_inorden_fb(nodoarbol *raiz)
        {
            if(raiz!=NULL)
            {
                despliega_inorden_fb(raiz->izq);
                cout<<raiz->info<<"-> "<<raiz->fb<<endl;
                despliega_inorden_fb(raiz->der);
            }
        }
 //DESPLIEGA EL ARBOL USANDO PREORDEN
        void despliega_preorden(nodoarbol*raiz)
        {
            if(raiz!=NULL)
            {
                cout<<raiz->info<<" ";
                despliega_preorden(raiz->izq);
                despliega_preorden(raiz->der);
            }
        }
 //DESPLIEGA EL ARBOL USANDO INORDEN
        void despliega_inorden(nodoarbol *raiz)
        {
            if(raiz!=NULL)
            {
                despliega_inorden(raiz->izq);
                cout<<raiz->info<<" ";
                despliega_inorden(raiz->der);
            }
        }
 //DESPLIEGA EL ARBOL USANDO POSTORDEN
        void despliega_postorden(nodoarbol *raiz)
        {
            if(raiz!=NULL)
            {
                despliega_postorden(raiz->izq);
                despliega_postorden(raiz->der);
                cout<<raiz->info<<" ";
            }
        }
//DESPLIEGA EL ARBOL USANDO NIVEL POR NIVEL
        struct nodo
        {
            int dato;
            nodo* sig;
        };
        void despliega_nivel_por_nivel(nodoarbol *raiz)
        {
            if(raiz!=NULL)
            {
                nodo *final,*temp,*nuevo;
                nodoarbol *apunt;
                nuevo=new nodo;
                nuevo->dato=raiz->info;
                final=nuevo;
                temp=nuevo;
                apunt=raiz;
                final->sig=NULL;
                while(temp!=NULL)
                {
                    cout<<temp->dato<<" ";
                    if(apunt->izq!=NULL)
                    {
                        nuevo=new nodo;
                        final->sig=nuevo;
                        nuevo->dato=apunt->izq->info;
                        final=nuevo;
                        final->sig=NULL;
                        if(apunt->der!=NULL)
                        {
                            nuevo=new nodo;
                            final->sig=nuevo;
                            nuevo->dato=apunt->der->info;
                            final=nuevo;
                            final->sig=NULL;
                        }
                    } 
                    else
                    {
                        if(apunt->der!=NULL)
                        {
                            nuevo=new nodo;
                            final->sig=nuevo;
                            nuevo->dato=apunt->der->info;
                            final=nuevo;
                            final->sig=NULL;
                        }
                    } 
                    temp=temp->sig;
                    if(temp!=NULL)
                    {
                        comparar_nodo_a_nodo(raiz,temp->dato);
                        apunt=resultado;
                    }
                }
            } 
            else
            {
                cout<<"\n El arbol esta vacio"<<endl;
            }
        }
        nodoarbol *resultado;
        void comparar_nodo_a_nodo(nodoarbol *raiz,int valor)
        {
            if(raiz!=NULL)
            {
                comparar_nodo_a_nodo(raiz->izq,valor);
                if(raiz->info==valor)
                {
                    resultado=raiz;
                } 
                else
                {
                    comparar_nodo_a_nodo(raiz->der,valor);
                }
            }
        } 
//eliminar
        void eliminar_nodo()
        {
            nodoarbol *aux1,*aux2,*temp;
            bool b;
            int valor;
            cout<<"-Entre el valor del nodo a eliminar: ";
            cin>>valor;
            //Inicia la busqueda del nodo a eliminar
            aux1=raiz;
            aux2=NULL;
            while(aux1->info!=valor)
            {
                aux2=aux1;
                if(valor<aux1->info)
                {
                    aux1=aux1->izq;
                }
                else
                {
                    aux1=aux1->der;
                }
                if(aux1==NULL)
                {
                    cout<<"El nodo no existe en el arbol"<<endl;
                    break;
                }
            } 
            //Fin de la busqueda del nodo aeliminar
            //en aux1 queda la direccion del nodo a eliminar
            //en aux2 queda la direccion del nodo padre del nodo a eliminar
            if(aux1!=NULL)
            {
                temp=aux1;
                //cuando no tiene hijos
                if((aux1->izq==NULL)&&(aux1->der==NULL))
                {
                    if(aux2!=NULL)
                    {
                        if(aux1->info>aux2->info)
                        {
                            aux2->der=NULL;
                        }
                        else
                        { 
                            aux2->izq=NULL;
                        }
                    } 
                    else
                    {
                        raiz=NULL;
                    }
                } 
                else
                {
                //cuando tiene dos hijos
                    if((aux1->izq!=NULL)&&(aux1->der!=NULL))
                    {
                        int num = 0;
                        cout<<"Si desea remplazar con el predecesor marque 1"<<endl<<endl;
                        cout<<"Si desea remplazar con el sucesor marque 2"<<endl;
                        cin>>num;
                        if(num==1)
                        {
                            aux2=aux1;
                            temp=aux1->izq;
                            b=true;
                            while(temp->der!=NULL)
                            {
                                aux2=temp;
                                temp=temp->der;
                                b=false;
                            }
                            aux1->info=temp->info;
                            if(b==true)
                            {
                                aux1->izq=temp->izq;                        
                            }
                            else
                            {
                                if(temp->izq!=NULL)
                                {
                                    aux2->der=temp->izq;
                                }
                                else
                                {
                                    aux2->der=NULL;
                                }
                            }
                        }
                        else
                        {
                            if(num==2)
                            {
                                aux2=aux1;
                                temp=aux1->der;
                                b=true;
                                while(temp->izq!=NULL)
                                {
                                    aux2=temp;
                                    temp=temp->izq;
                                    b=false;
                                }
                                aux1->info=temp->info;
                                if(b==true)
                                {
                                    aux1->der=temp->der;
                                }
                                else
                                {
                                    if(temp->izq!=NULL)
                                    {
                                        aux2->izq=temp->der;
                                    }
                                    else 
                                    {
                                        aux2->izq=NULL;
                                    }
                                }
                            }
                            else 
                            {
                                cout<<"La opcion no escorrecta"<<endl<<endl;
                            }
                        }
                    } 
                    else
                    {
                    //cuando tiene un solo hijo
                        if(aux1->izq==NULL)
                        {
                            if(aux2!=NULL)
                            {
                            if(aux1->info<aux2->info) 
                            {
                                aux2->izq=aux1->der;
                            }
                            else 
                            {
                                aux2->der=aux1->der;
                            }
                            } 
                            else
                            {
                                raiz=aux1->der;
                            } 
                        } 
                        else
                        {
                            if(aux2!=NULL)
                            {
                                if(aux1->info<aux2->info) 
                                {
                                    aux2->izq=aux1->izq;
                                }
                                else 
                                {
                                    aux2->der=aux1->izq;
                                }
                            } 
                            else 
                            {
                                raiz=aux1->izq;
                            }
                        }
                    }
                } 
                delete temp;
                factor_de_balanceo(raiz);//aqui asigno el Factor deBalanceo //(fb) para el nuevo arbol
                balancear(raiz);//aqui balanceo el arbol
                factor_de_balanceo(raiz);//aqui asigno el FB despues de //balancearlo
                balancear(raiz);//aqui balanceo el arbol
            }
            system("pause");
        }
    };
int main()
{
    nodoarbol *raiz;
    int opc;
    AVL n;
    do
    {
        raiz=n.devolver_raiz();
        cout<<"\n************MENU PRINCIPAL*****************"<<endl;
        cout<<"1. Agregar elementos al arbol"<<endl;
        cout<<"2. Desplegar los elementos en inorden"<<endl;
        cout<<"3. Desplegar los elementos en postorden"<<endl;
        cout<<"4. Desplegar los elementos en preorden"<<endl;
        cout<<"5. Desplegar los elementos nivel por nivel"<<endl;
        cout<<"6. Eliminar elementos del arbol"<<endl;
        cout<<"7. Salir"<<endl;
        cout<<"*******************************************"<<endl;
        cin>>opc;
        switch(opc)
        {
            case 1:
                //int resp;
                char res;
                do
                {
                    n.insertar();
                    cout<<"1. Desea agregar otro nodo (s/n) \n"<<endl;
                    cin>>res;
                }while(res=='s');
                break;
            case 2:
                if(raiz!=NULL)
                {
                    n.despliega_inorden(raiz);
                }
                else 
                {
                    cout<<" El arbol esta vacio"<<endl;
                }
                system("pause");
                break;
            case 3:
                if(raiz!=NULL)
                {
                    n.despliega_postorden(raiz);
                }
                else 
                {
                    cout<<" El arbol esta vacio"<<endl;
                }
                system("pause");
                break;
            case 4:
                if(raiz!=NULL)
                {
                    n.despliega_preorden(raiz);
                }
                else 
                {
                    cout<<" El arbol esta vacio"<<endl;
                }
                system("pause");
                break;
            case 5:
                n.despliega_nivel_por_nivel(raiz);
                system("pause");
                break;
            case 6:
                n.eliminar_nodo();
                break;
            case 7:
                //exit(0);
                break;
            default:
                cout<<"Lo sentimos, "<<opc<<" no es una opcionvalida, por favor intente de nuevo"<<endl;
                system("pause");
                break;
        }
    }while(opc!=7);
    _getch();
}

