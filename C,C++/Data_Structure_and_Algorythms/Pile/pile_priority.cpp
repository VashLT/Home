#include <iostream>

using namespace std;

struct nodo
{
    int data;
    int priority = 0;
    nodo *next;
};

class Pile
{
    private:
        nodo *last;
    public:
        void add(bool priority = false);
        void quit();
        Pile();
        ~Pile();
        void clean();
        void showLast();
        void length();
        void show();
        void menu();
        bool checkRepeat(int key);
        nodo *lastNode();
        nodo *searchPriority(int priority);
};

Pile::Pile()
{
    this->last = NULL;
}

Pile::~Pile()
{
    while(this->last != NULL)
			{
				nodo *aux = this->last;
				this->last = this->last->next;
				cout<<"Deleting node with dato = "<<aux->data<<endl;
				delete aux;
			}
}

void Pile::add(bool priority)
{
    nodo *new_node,*priorityNode;
    char ans;
    bool repeat = false;
    do
    {
        new_node = new nodo();

        do
        {
            cout<<"Enter the key of the node to add: ";
            cin>>new_node->data;
            if(priority)
            {
                cout<<"Enter the priority of the node: (default: 0) "<<endl; //set a priority
                cin>>new_node->priority;
            }
            if(this->last == NULL)
            {
                break;
            }
            repeat = checkRepeat(new_node->data);
        } while (repeat == false);

        if(this->last == NULL) //add the first node
        {
            new_node->next = NULL;
            this->last = new_node;
        }
        else
        {
           
            priorityNode = searchPriority(new_node->priority); 
            if(priorityNode == NULL) //add a node with min priority
            {
                if(new_node->priority > this->last->priority)
                {
                    new_node->next = this->last;
                    this->last = new_node;
                }
                else
                {
                    priorityNode = lastNode();
                    priorityNode->next = new_node;
                    new_node->next = NULL;
                }
            }
            else
            {
                if(this->last == priorityNode)
                {
                    new_node->next = this->last;
                    this->last = new_node;
                }
                else
                {
                    new_node->next = priorityNode->next;
                    priorityNode->next = new_node; 
                }
            }
        }
        cout<<"Do you want to add another node? (y/n) "<<endl;
        cin>>ans;
    } while (ans != 'n');
    
};
void Pile::quit()
{
    nodo *toDelete;
    if(this->last != NULL)
    {
 
        toDelete = this->last;
        this->last = this->last->next;   
        delete toDelete;
    }
    else
    {
        cout<<"THe pile is empty."<<endl;
    }
    
}
void Pile::clean()
{
    if(this->last != NULL)
    {
        cout<<"Cleanining..."<<endl;
        while(this->last != NULL)
        {
            nodo *cleaner = this->last;
            this->last = this->last->next;
            cout<<cleaner->data<<" was succesfully cleaned."<<endl;
            delete cleaner;
        }
    }
    else
    {
        cout<<"The pile is already cleaned."<<endl;
    }
    
};
void Pile::showLast()
{
    if(this->last != NULL)
    {
        cout<<"The last node is "<<this->last->data<<endl;
    }
    else
    {
        cout<<"The list is empty."<<endl;
    }
}
void Pile::length()
{
    nodo *traveler;
    int length=0;
    if(this->last != NULL)
    {
        traveler = this->last;
        while(traveler != NULL)
        {
            length++;
            traveler = traveler->next;
        }
        cout<<"Length: "<<length<<endl;
    }
    else
    {
        cout<<"Length: 0"<<endl;
    }
    
}
void Pile::show()
{
    nodo *traveler;
    if(this->last != NULL)
    {
        traveler = this->last;
        while(traveler != NULL)
        {
            cout<<traveler->data<<" ";
            traveler = traveler->next;
        }
        cout<<endl;
    }
    else
    {
        cout<<"The pile is empty."<<endl;
    }
    
}
bool Pile::checkRepeat(int key)
{
    nodo *traveler = this->last;
    if(traveler->data == key)
    {
        cout<<"The node to add is already in the pile."<<endl;
        return false;
    }
    else
    {
        while(traveler != NULL)
        {
            if(traveler->data == key)
            {
                cout<<"The node to add is already in the pile."<<endl;
                return false;
            }
            traveler = traveler->next;
        }
        return true;
    }
    
}
nodo* Pile::searchPriority(int priority)
{
    nodo *traveler = this->last;
    while(traveler != NULL)
    {
        if(traveler->next != NULL && priority > traveler->next->priority)
        {
            return traveler;
        }
        traveler = traveler->next;
    }

    return NULL;
}
nodo* Pile::lastNode()
{
    nodo* traveler = this->last;
    while(traveler->next != NULL)
    {
        traveler = traveler->next;
    }
    return traveler;
}
void Pile::menu()
{
    int ans;
    do
    {
        cout<<"Enter the option: "<<endl;
        cout<<"1. add a node to the pile"<<endl;
        cout<<"2. remove a node from the pile"<<endl;
        cout<<"3. show the last node "<<endl;
        cout<<"4. show all the nodes in the pile."<<endl;
        cout<<"5. Clean pile."<<endl;
        cout<<"6. Length of the pile."<<endl;
        cout<<"7. Exit"<<endl;
        cin>>ans;
        if(ans >0 && ans<8)
        {
            switch (ans)
            {
            case 1:
                char prior_opc;
                cout<<"With priority? (y/n) :"<<endl;
                cin>>prior_opc;
                if(prior_opc == 'n')
                {
                    add();
                }
                else
                {
                    add(true);
                }
                break;
            case 2:
                quit();
                break;
            case 3:
                showLast();
                break;
            case 4:
                show();
                break;
            case 5:
                clean();
                break;
            case 6:
                length();
                break;
            case 7:
                break;
            }
        }
        else
        {
            cout<<"The entered option is not available."<<endl;
        }
         
    } while (ans != 7);
    
}
int main()
{
    Pile pile;
    pile.menu();

    delete &pile;
    system("pause");
}