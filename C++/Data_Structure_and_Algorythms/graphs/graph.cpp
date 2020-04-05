#include <iostream>
#include <vector>
#include <stdlib.h>
#include <string>
using namespace std;

void print( string s)
{
   int LINELENGTH = 80;
   string header( LINELENGTH, '=' );
   cout<< header << "\n";
   int spaces = 0;
   spaces = ( LINELENGTH - s.size() ) / 2;  
   if ( spaces > 0 ) cout << string( spaces, ' ' );

   cout << s << '\n';
   cout << header << "\n";
}

struct Node
{
    int data;
    vector<Node*> adjacent_nodes;
};

struct Edge
{
    Node *src,*dest ;  
    int weight;
};

class Graph
{
    private:
        vector<Edge*> edge_list;
        vector<Node*> vertex_list;

        //return true if the vertex is in the graph
        Node *query_vertex(int value)
        {
            if(! this->vertex_list.empty())
            {
                for (Node *vertex : this->vertex_list )
                {
                    if( vertex->data == value) return vertex;
                }
            }
            return NULL;
        }
    public:
        Graph(int data)
        {
            Node *first_node = new Node();
            first_node->data = data;
            this->vertex_list.push_back(first_node);
            update_adj_list(first_node, NULL);
        }
        ~Graph()
        {
            for(Node *node : this->vertex_list)
            {
                cout<<"deleting node with data "<<node->data<<endl;
                delete node;
            }
        }
        void add_vertex(int data)
        {
            Node *node = new Node();
            int vertex_value;
            Node *temp;

            //adding the node
            node -> data = data;
            this->vertex_list.push_back(node);

            cout<<"Enter the vertex connecitons : "<<endl;
            cout<<"Input connecitons: "<<endl;
            //stop when enter a non-integer value
            while ( (cin >> vertex_value) && vertex_value != 9999)
            {
                temp = query_vertex(vertex_value);
                if( temp != NULL)
                {
                    add_edge(temp, node);
                    update_adj_list(node, this->edge_list.back());
                    cout<<"to exit press 9999."<<endl;
                }
                else cout<<"the vertex is not in the graph"<<endl;
            }
            cout<<"Output connections: "<<endl;
            while ( (cin >> vertex_value) && vertex_value != 9999)
            {
                temp = query_vertex(vertex_value);
                if( temp != NULL)
                {
                    add_edge(node, temp); 
                    update_adj_list(node, this->edge_list.back(), false);
                }
                else cout<<"the vertex is not in the graph"<<endl;
            }
            
           

        };
        void add_edge(Node *src, Node *dest)
        {
            cout<<"adding edge..."<<endl;
            Edge *edge = new Edge();
            edge->src = src;
            edge->dest = dest;
            this->edge_list.push_back(edge);
            cout<<"edge: ["<<edge->src->data<<"] --> ["<<edge->dest->data<<"] succesfully added!!."<<endl;
        }
        bool are_connected(Node *node1, Node*node2)
        {
            cout<<"check if are connected.";
            for(Edge *edge : this->edge_list)
            {
                if (((edge->src == node1) | (edge->dest == node1)) && ((edge->dest == node2) | (edge->src == node2)))
                {
                    return true;
                }
            }
            return false;
        };
        void delete_vertex();
        void print_graph()
        {
            for(Node *node : this->vertex_list)
            {
                cout<<node->data<<" --> ";
                for(int i=0; i< node->adjacent_nodes.size(); i++)
                {
                    cout<<node->adjacent_nodes[i]->data;

                    if (i < node->adjacent_nodes.size()-1)
                    {
                      cout<<"->";  
                    }
                }
                cout<<endl;
            }
        };
        void update_adj_list(Node *node, Edge *edge, bool enter_edge = true )
        {
            if(edge != NULL)
            {
                if(enter_edge)
                {
                    
                    edge->src->adjacent_nodes.push_back(node);
                    
                }
                else{
                    
                    node->adjacent_nodes.push_back(edge->dest);
                    
                }
            }
        };
        void menu()
        {
            int opc = 0;
            char ans;
            while(opc != 3)
            {
                system("cls");
                print("MENU");
                cout<<"Enter: "<<endl;
                cout<<"1 -> Agregar un vertice"<<endl;
                cout<<"2 -> Imprimir el grafo"<<endl;
                cout<<"3 -> Salir"<<endl;
                cin>> opc;
                if (opc == 1)
                {
                    int vertex_value;
                    system("cls");
                    cout<<"Enter the vertex value: ";
                    cin>>vertex_value;
                    add_vertex(vertex_value);
                    system("pause");
                }
                else if (opc == 2)
                {
                    print_graph();
                    system("pause");
                }
            }
        }
};

int main(){
    Graph graph(20);
    graph.menu();

    system("pause");
}