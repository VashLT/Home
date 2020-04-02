#include <iostream>
#include <iomanip>
#include <windows.h>

using namespace std;

class NodoArbol {

    public:
    int info;
    NodoArbol *der, *izq;

    NodoArbol(){
        info = 0;
        izq = NULL;
        der = NULL;
    }

    NodoArbol(int dato){
        info = dato;
        izq = NULL;
        der = NULL;
    }
};

class ABB{

    private:
    NodoArbol *raiz;

    public:

    ABB(){
        raiz = NULL;
    }

    ~ABB(){
        if(raiz != NULL)
        {
            int temp;
            cout << "Digite el orden en el que se va a liberar la memoria: " << endl;
            cout << "1. Preorden" << endl;
            cout << "2. Inorden " << endl;
            cout << "3. Postorden " << endl;
            cin >> temp;
            borrarNodos(raiz,temp); 
        }
    }

    void borrarNodos(NodoArbol *raiz,int tipo){
        switch(tipo)
        {
            case 1:
                if(raiz != NULL){
                cout << "Liberando la memoria de  "<<raiz->info<< endl;  
                borrarNodos(raiz->izq,1);
                borrarNodos(raiz->der,1); 
                delete raiz;
                }
                break;
            case 2:
                if(raiz != NULL){
                borrarNodos(raiz->izq,2);
                cout << "Liberando la memoria de  "<<raiz->info<< endl;
                borrarNodos(raiz->der,2);    
                delete raiz; 
                }
                break;
            case 3:
                if (raiz != NULL){
                borrarNodos(raiz->izq,3);
                borrarNodos(raiz->der,3);
                cout << "Liberando la memoria de  "<<raiz->info<< endl;   
                delete raiz; 
                }
                break;
            case 4:
                break;   
        }           
    }
    void insertar(){
        NodoArbol *nuevo, *aux2, *aux3,*check;

        nuevo = new NodoArbol();
        
        aux2 = raiz;
        aux3 = NULL;

        do{

        cout << "Entre el valor del nodo a insertar: ";
        cin >> nuevo->info;
        check = Buscar(nuevo->info);
        if(check != NULL)
        {
           cout << "El nodo a insertar ya existe." << endl; 
        }
        }while( check != NULL );


        while (aux2 != NULL){
            aux3 = aux2;
            if(nuevo->info > aux2->info){
                aux2 = aux2->der;
            } else {
                aux2 = aux2->izq;
            }
        }

        if(aux3 == NULL){
            // Si el arbol esta vacio
            raiz = nuevo;
        } else {
            if(nuevo->info >= aux3->info){
                aux3->der = nuevo;
            } else {
                aux3->izq = nuevo;
            }
        }
                
    }

    NodoArbol *obtenerRaiz(){
        return raiz;
    }
    
    void despliega(NodoArbol *raiz, int tipo){
        // tipo 1: preorden
        // tipo 2: inorden
        // tipo 3: postorden
        // tipo 4: nivel por nivel
        switch(tipo)
        {
            case 1:
                if (raiz != NULL){
                cout <<raiz->info << " " << endl;
                despliega(raiz->izq,1);
                despliega(raiz->der,1);   
                }  
                break;
            case 2:
                if (raiz != NULL){
                despliega(raiz->izq,2);
                cout <<raiz->info << " " << endl;
                despliega(raiz->der,2);
                }     
                break;
            case 3:
                if (raiz != NULL){
                despliega(raiz->izq,3);
                despliega(raiz->der,3);   
                cout <<raiz->info << " " << endl; 
                } 
                break;
            case 4:
                desplegarAmplitud(obtenerRaiz());
                break;   
        }
    }
    NodoArbol *Buscar(int dato){
        NodoArbol *buscar,*temp;
        temp = NULL;
        buscar = obtenerRaiz();
        while (buscar != NULL)
        {
            if(buscar->info == dato)
            {
                return buscar;
            }
            else if(dato > buscar->info){
                buscar = buscar->der;
            } else {
                buscar = buscar->izq;
            }
        }
        return buscar;
    }

    bool desplegarNivel(NodoArbol *raiz, int nivel){
        
        if (raiz == NULL){
            return false;
        }

        if (nivel == 1){
            cout << raiz->info << " ";
            return true;
        }   

        bool izq = desplegarNivel(raiz->izq, nivel - 1);
        bool der = desplegarNivel(raiz->der, nivel - 1);

        return izq || der;
    }
    
    void desplegarAmplitud(NodoArbol *raiz){
        int nivel = 1;

        while (desplegarNivel(raiz, nivel))
        {
            nivel++;
            cout << endl;
        }
    }
    void eliminarValor(int valor){

        NodoArbol *aux1, *aux2, *temp;
        bool b;

        //Inicio de busqueda del nodo a eliminar

        if(raiz != NULL){
            aux1 = raiz;
            aux2 = NULL;

            while(aux1->info != valor){
                aux2 = aux1;

                if(valor < aux1->info){
                    aux1 = aux1->izq;
                } else {
                    aux1 = aux1->der;
                }

                if(aux1==NULL){
                    cout << "El nodo a eliminar no existe" << endl;
                    break;
                }
            }
        } else {
            cout << "El arbol no contiene nodos" << endl;
            aux1 = NULL;
        }

        //Fin de la busqueda del nodo a eliminar
        // En aux1 queda la direccion del nodo a eliminar
        // En aux2 queda la direccion del nodo padre del nodo a eliminar

        if (aux1 != NULL) // Cuando no tiene hijos
        {
            temp = aux1;
            if ((aux1->izq == NULL) && (aux1->der==NULL))
            {
                if (aux2 != NULL)
                {
                    if (aux1->info > aux2->info)
                    {
                        aux2->der = NULL;
                    }
                    else 
                    {
                        aux2->izq = NULL;
                    }
                } 
                else 
                {
                    raiz = NULL;
                }
            } 
            else 
            {
                
                if((aux1->izq != NULL) && (aux1->der != NULL))  // Cuando tiene dos hijos
                {        
                    char resp;  
                    cout<<"El nodo que se quiere eliminar tiene dos hijos, desea reemplazarlo con el predecesor? (s/n)" << endl;
                    cin >> resp;
                    resp = tolower(resp);
                    aux2 = aux1;
                    b = true;
                    if(resp == 's')
                    {
                        temp = aux1->izq; // se reemplaza con el predecesor

                        while(temp->der != NULL){
                            aux2 = temp;
                            temp = temp->der;
                            b=false;
                        }

                        aux1->info = temp->info;
                        if(b == true){
                            aux1->izq = temp->izq;
                        } 
                        else {

                            if(temp->izq != NULL)
                            {
                                aux2->der = temp->izq;
                            } 
                            else 
                            {
                                aux2->der = NULL;
                            }
                        }
                        cout << "Se eliminó el nodo con el predecesor ." << temp->info << endl; 
                    }
                    else // se reemplaza con el sucesor
                    {
                        temp = aux1->der;

                        while(temp->izq != NULL)
                        {
                            aux2 = temp;
                            temp = temp->izq;
                            b = false;
                        }
                        aux1->info = temp->info;
                        if ( b == true )
                        {
                            aux1->der = temp->der;
                        }
                        else
                        {
                            if (temp->der != NULL)
                            {
                                aux2->izq = temp->der;
                            }
                            else
                            {
                                aux2->izq = NULL;
                            }
                            
                        }
                        cout << "Se eliminó el nodo con el sucesor ." << temp->info << endl; 
                        
                    }
                    
                    
                } 
                else  //Cuando tiene solo un hijo
                {
                    if (aux1->izq == NULL)
                    {
                        if (aux2 != NULL)
                        {
                            if (aux1->info < aux2->info)
                            {
                                aux2->izq = aux1->der;
                            }
                            else 
                             {
                                aux2->der = aux1->der;
                            }
                        } 
                        else
                        {
                            raiz = aux1->der;
                        }
                    }
                    else 
                    {
                        if (aux2 != NULL){
                            if (aux1->info < aux2->info)
                            {
                                aux2->izq = aux1->izq;
                            } 
                            else 
                            {
                                aux2->der = aux1->izq;
                            }
                        } 
                        else 
                        {
                            raiz = aux1->izq;
                        }
                    }
                }
            }

            delete temp;
        } 
    }
    void menu(){
        int opc;
        char resp;
        do
        {
            cout << " MENU " << endl << endl;
            cout <<"Opciones: " << endl << endl;
            cout << "1. agregar un nodo." << endl << endl;
            cout << "2. Eliminar un nodo"<< endl << endl;
            cout << "3. Desplegar el arbol." << endl << endl;
            cout << "4. Salir"<<endl;
            cout << "Digite la opcion: ";
            cin >> opc;
            if(opc >0 && opc<5)
            {
                switch (opc)
                {
                case 1:
                    do {
                        insertar();
                        cout << "Desea agregar otro nodo? S/N: " << endl;
                        cin >> resp;
                        resp = tolower(resp);
                    }while(resp != 'n');
                    break;
                case 2:
                    int valor;
                    do {
                        cout << "Entre el valor del nodo a eliminar: " << endl;
                        cin >> valor;
                        eliminarValor(valor);
                        cout << endl;
                        cout << "Desea eliminar otro nodo? S/N: "<<endl;
                        cin >> resp;
                        cout << endl;
                        resp = tolower(resp);
                    }while(resp != 'n');
                    break;
                case 3:
                    int ans;
                    cout << "Como desea desplegar el arbol?: " << endl;
                    cout << "1. Preorden" << endl;
                    cout << "2. Inorden " << endl;
                    cout << "3. Postorden " << endl;
                    cout << "4. Por nivel " << endl;
                    cout << "Opcion: ";
                    cin >> ans;
                    despliega(obtenerRaiz(),ans);
                    break;
                case 4:
                    break;
                }
            }
            else
            {
                cout<<"La opción digitada no esta disponible."<<endl;
            }
        } while (opc != 4);
    }
};


int main(){

    NodoArbol *raiz;
    char resp;
    int valor;
    ABB n;
    n.menu();
}