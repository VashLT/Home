// Double circular linked list

#include <iostream>

using namespace std;

struct nodo
{
    int dato;
    nodo *next;
    nodo *prev;
};
class circularLinkedList
{
    private:
        nodo *head;
        nodo *search(int key, bool deleteMode = false);
        nodo *searchTail();
    public:
        circularLinkedList(); //construct
        ~circularLinkedList(); //finalizer
        void add();
        void showList();
        void remove();
        void menu();
        bool checkRepeat(int key);
};

circularLinkedList::circularLinkedList()
{
    this->head = NULL;    
};
circularLinkedList::~circularLinkedList()
{
    nodo *temp = searchTail();
    temp->next = NULL;
    while(this->head != NULL)
        {
            nodo *aux = this->head;
            this->head = this->head->next;
            cout<<"Deleting node with dato = "<<aux->dato<<endl;
            delete aux;
        }
}
void circularLinkedList::showList()
{
    if(this->head == NULL)
    {
        cout<<"The list is empty."<<endl;
    }
    else
    {
        int ans;
        nodo *apunt;
        cout<<"Digite 1: para desplegar en sentido horario"<<endl;
        cout<<"       2: para desplegar en sentido anti horario"<<endl;
        cin>>ans;
        if(ans == 1)
        {
            apunt = this->head;
            do 
            {
                cout<<apunt->dato<<" ";
                apunt = apunt->next;
            }while(apunt != this->head);
        }
        else{
            apunt = this->head->prev;
            do
            {
                cout<<apunt->dato<<" ";
                apunt = apunt->prev;
            } while (apunt!= this->head);
            cout<<this->head->dato<<" ";
            
        }
        
    }
    cout<<endl;
}

nodo *circularLinkedList::search(int key, bool deleteMode)
{
    nodo *previous;
    previous = NULL;
    if(key == this->head->dato)
    {
        return this->head->prev;
    }
    else if(key < this->head->dato)
    {
        if(deleteMode == true)
        {
            if(this->head->dato != key)
            {
                return NULL;
            }
            else
            {
               return this->head; 
            }
        }
        return previous;
    }
    else
    {
        previous = this->head;
        while((key > previous->next->dato) && (previous ->next != this->head))
        {
            previous = previous->next;
        }
        if ( deleteMode == true)
        {
            if ( previous->next->dato != key)
            {
                return NULL;
            }
        }
        cout<<"previous: "<<previous->dato<<endl;
        return previous;
    }
}

nodo *circularLinkedList::searchTail()
{
    nodo *tail;
    tail = this->head;
    while( tail->next != this->head )
    {
        tail = tail->next;
    }
    return tail;
}

bool circularLinkedList::checkRepeat(int key)
{
    nodo *traveler = this->head;
    if(traveler->dato == key)
    {
        cout<<"The node to add already exists."<<endl;
        return false;
    }
    else
    {
        do
        {
            if(traveler->dato == key)
            {
                cout<<"The node to add already exists."<<endl;
                return false;
            }
            traveler = traveler->next;
        }while( traveler != this->head );
        return true;
    }  
}
void circularLinkedList::remove()
{
    nodo *temp,*toDelete;
    int key;
    char ans;
    cout<<"Do you want to eliminate a node? (y/n): "<<endl;
    cin>>ans;
    while(ans != 'n')
    {
        if(this->head != NULL)
        {
            cout<<"Enter the key of the node to eliminate: "<<endl;
            cin>>key;
            temp = search(key,true);
            if(temp == this->head)
            {
                if( this->head->next != this->head)
                {
                    toDelete = this->head->next;
                    toDelete->next->prev = this->head;
                    this->head->next = toDelete->next;
                       
                }
                else
                {
                    toDelete = this->head;
                    this->head = NULL;
                }
                cout<<toDelete->dato<<" was succesfully deleted."<<endl;
                delete toDelete;
            }
            else if(temp != NULL)
            {
                toDelete =  temp->next;
                if(temp->next == this->head) //if the node to eliminate is the head
                {
                    this->head = temp->next->next;
                    this->head->prev = temp;
                    temp->next = this->head;
                }
                else{
                    toDelete->next->prev = temp;
                    temp->next = temp->next->next;
                }
                cout<<toDelete->dato<<" was succesfully deleted."<<endl;
                delete toDelete;
            }
            else
            {
                cout<<"The node to eliminate does not exist."<<endl;
            }
        }
        else
        {
            cout<<"the list is empty."<<endl;
            break;
        }   
        cout<<"Do you want to eliminate another node? (y/n): "<<endl;
        cin>>ans;
    } 
}
     

void circularLinkedList::add()
{
    nodo *newNode,*previous;
    bool repeat=false;
    char ans;
    do
    {
        newNode = new nodo();
        do
        {
            cout<<"Enter the key of the node to add: "<<endl;
            cin>>newNode->dato;
            if(this->head == NULL) //check if the list is empty, this solves the problem where head is null and search makes NULL->next
            {
                break;
            }
            repeat = checkRepeat(newNode->dato); //check if exists a node with the code.
        }while(repeat == false);
        if(this->head == NULL) //if the list is empty
        {
            this->head = newNode;
            newNode->prev = newNode;  //add the first node to the list
            newNode->next = newNode;
        }
        else
        {
            previous = search(newNode->dato); //search for the node that is just before the new node to add.
            if(previous == NULL) //if the node was not found or the node is less than the head.
            {
                this->head->prev->next = newNode;
                newNode->prev = this->head->prev;
                newNode->next = this->head;
                this->head->prev = newNode;
                this->head = newNode;
            }
            else //add a node that is not the head 
            {
                previous->next->prev = newNode;
                newNode->next = previous->next;
                newNode->prev = previous;
                previous->next = newNode;
            }
            
        }
        cout<<"Do you want to add another node? (y/n)"<<endl;
        cin>>ans;
        ans = tolower(ans);
        
    } while (ans != 'n');
}
void circularLinkedList::menu()
{
    int opc;
    do
    {
        cout<<" ***WELCOME TO THE MENU*** "<<endl;
        cout<<"Options: "<<endl;
        cout<<"1. Create a list."<<endl;
        cout<<"2. Eliminate a node."<<endl;
        cout<<"3. Show list."<<endl;
        cout<<"4. Exit"<<endl;
        cout<<"Enter the option: "<<endl;
        cin>>opc;
        if(opc >0 && opc<5)
        {
            switch (opc)
            {
            case 1:
                add();
                break;
            case 2:
                remove();
                break;
            case 3:
                showList();
                break;
            case 4:
                break;
            }
        }
        else
        {
            cout<<"The entered option is not available."<<endl;
        }
    } while (opc != 4);
    
    
}

int main()
{
    circularLinkedList list;
    list.menu();

    delete &list;
    system("pause");
}