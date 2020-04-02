// Double linked list

#include <iostream>

using namespace std;

struct nodo
{
    int dato;
    nodo *prev;
    nodo *next;
};
class linkedList
{
    private:
        nodo *head;
        nodo *search(int key, bool deleteMode = false);
    public:
        linkedList(); //construct
        ~linkedList(); //finalizer
        void add();
        void showList();
        void remove();
        void menu();
        bool checkRepeat(int key);
};

linkedList::linkedList()
{
    this->head = NULL;    
};
linkedList::~linkedList()
{
    while(this->head != NULL)
			{
				nodo *aux = this->head;
				this->head = this->head->next;
				cout<<"Deleting node with dato = "<<aux->dato<<endl;
				delete aux;
			}
}
void linkedList::showList()
{
    if(head == NULL)
    {
        cout<<"The list is empty."<<endl;
    }
    else
    {
        nodo *apunt;
        apunt = this->head;
        while(apunt != NULL) //travel the list.
        {
            cout<<apunt->dato<<" ";
            apunt = apunt->next;
        }
    }
    cout<<endl;
}

nodo *linkedList::search(int key, bool deleteMode)
{
    nodo *previous;
    previous = NULL;
    if(key <= this->head->dato)
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
        while((previous ->next != NULL) && (key > previous->next->dato))
        {
            previous = previous->next;
        }
        if ( deleteMode == true)
        {
            if (previous->next == NULL)
            {
                return NULL;
            }
            else if ( previous->next->dato != key)
            {
                return NULL;
            }
        }
        cout<<"data: "<<previous->dato<<endl;
        return previous;
    }
}

bool linkedList::checkRepeat(int key)
{
    nodo *traveler = this->head;
    if(traveler->dato == key)
    {
        cout<<"The node to add already exists."<<endl;
        return false;
    }
    else
    {
        while( traveler != NULL )
        {
            if(traveler->dato == key)
            {
                cout<<"The node to add already exists."<<endl;
                return false;
            }
            traveler = traveler->next;
        }
        return true;
    }  
}
void linkedList::remove()
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
                if( this->head->next != NULL)
                {
                    if(this->head->next->dato == key)
                    {
                        toDelete = this->head->next;
                        this->head->next->next->prev = this->head;
                        this->head->next = this->head->next->next;
                    }
                    else
                    {
                        toDelete = this->head;
                        this->head = this->head->next;
                        this->head->prev = NULL; //check
                    }
                    
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
                if(temp->next->next != NULL)
                {
                    temp->next->next->prev = temp;
                    temp->next= temp->next->next;
                }
                else{ // if temp->next->next == NULL means that temp->next is the tail node
                    temp->next = NULL; // so, we are going to delete temp->next, and temp is going to be the tail node now.
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
     

void linkedList::add()
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
            this->head = newNode; //add the first node to the list
            newNode->next = NULL;
            newNode->prev = NULL;
        }
        else
        {
            previous = search(newNode->dato); //search for the node that is just before the new node to add.
            if(previous == NULL) //if the node was not found or the node is less than the head.
            {
                newNode->next = this->head;
                newNode->prev = this->head->prev;
                this->head->prev = newNode;
                this->head = newNode;
            }
            else 
            {
                if(previous->next != NULL) //add the node between the head and the tail.
                {
                    newNode->next = previous->next;
                    newNode->prev = previous;
                    previous->next->prev = newNode;
                    previous->next = newNode;
                }
                else //add the node to the last position. 
                {
                    newNode->next = NULL;
                    newNode->prev = previous;
                    previous->next = newNode;
                }
            }
            
        }
        cout<<"Do you want to add another node? (y/n)"<<endl;
        cin>>ans;
        ans = tolower(ans);
        
    } while (ans != 'n');
}
void linkedList::menu()
{
    int opc;
    do
    {
        cout<<" ***WELCOME TO THE MENU*** "<<endl<<endl<<endl;
        cout<<"Options: "<<endl<<endl;
        cout<<"1. Create a list."<<endl<<endl;
        cout<<"2. Eliminate a node."<<endl<<endl;
        cout<<"3. Show list."<<endl<<endl;
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
    linkedList list;
    list.menu();

    delete &list;
    system("pause");
}