#include <iostream>
#include <vector>
#include <stdlib.h>
#include <string>
#include <algorithm>
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
/*
    incident_degree: 0 if there's no incident edges
*/

struct Node
{
    int data, incident_degree = 0, adjacency_degree = 0;
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
        Node *query_vertex(int value, bool show_grade = false)
        {
            if(! this->vertex_list.empty())
            {
                for (Node *vertex : this->vertex_list )
                {
                    if( vertex->data == value)
                    {
                        if(show_grade)
                        {
                            cout<<"Incident degree: "<<vertex->incident_degree<<endl;
                            cout<<"Adjacency degree: "<<vertex->adjacency_degree<<endl;
                        }
                        return vertex;
                    }
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
            for(Edge *edge : this->edge_list)
            {
                cout<<"deleting edge  ["<<edge->src->data<<"] -> ["<<edge->src->data<<"]"<<endl;
                delete edge;
            }
        }
        void add_vertex(int data)
        {
            if(query_vertex(data) == NULL)
            {
                Node *node = new Node();
                int vertex_value;
                char ans;
                Node *temp;
                //adding the node
                node -> data = data;
                this->vertex_list.push_back(node);

                cout<<"Enter the vertex connecitons : "<<endl;
                do{
                    cout<<"Incident vertex: ";
                    cin>>vertex_value;
                    if(vertex_value == 0) break;
                    temp = query_vertex(vertex_value);
                    if( temp != NULL)
                    {
                        add_edge(temp, node);
                        update_adj_list(node, this->edge_list.back());
                    }
                    else{
                        cout<<"\nThe vertex is not in the graph. "<<endl;
                    } 

                    cout<<"\nAdd another connection? (y/n) ";
                    cin>>ans;
                    ans = tolower(ans);
                }while(ans != 'n');
                ans = 'y';
                do {
                    cout<<"Adjacent vertex: ";
                    cin>>vertex_value;
                    if(vertex_value == 0) break;
                    temp = query_vertex(vertex_value);
                    if( temp != NULL)
                    {
                        add_edge(node, temp); 
                        update_adj_list(node, this->edge_list.back(), false);
                    }
                    else cout<<"\nThe vertex is not in the graph. "<<endl;
                    cout<<"\nDo you want to add another connection? (y/n) ";
                    cin>>ans;
                    ans = tolower(ans);
                }while (ans != 'n');
            }
            else cout<<"A vertex with the value is already in the graph."<<endl;
        };

        void add_edge(Node *src, Node *dest)
        {
            cout<<"adding edge..."<<endl;
            Edge *edge = new Edge();
            edge->src = src;
            edge->dest = dest;
            this->edge_list.push_back(edge);
            src->adjacency_degree++;
            dest->incident_degree++;
            cout<<"edge: ["<<edge->src->data<<"] --> ["<<edge->dest->data<<"] succesfully added!!."<<endl;
        }
        bool are_connected(Node *node1, Node*node2)
        {
            for(Edge *edge : this->edge_list)
            {
                if (((edge->src == node1) | (edge->dest == node1)) && ((edge->dest == node2) | (edge->src == node2)))
                {
                    return true;
                }
            }
            return false;
        };
        void delete_vertex(int value, bool strong = false)
        {
            Node *node = query_vertex(value);
            if(node != NULL)
            {
                if (node->adjacency_degree > 0 | node->incident_degree > 0)
                {
                    int index = 0, position;
                    vector<Node*>::iterator iter;

                    //for(Node *ady : node->adjacent_nodes)
                    //{
                    index = 0;
                        //check the edges that links the nodes to delete them.
                    for(Edge *edge : this->edge_list)
                    {
                        if(edge->src == node)
                        {
                            cout<<"Deleting edge ["<<node->data<<"] -> ["<<edge->dest->data<<"] ..."<<endl;
                            this->edge_list.erase( this->edge_list.begin() + index);
                            index--;
                            edge->dest->incident_degree--;
                            delete edge;
                        }
                        else if(edge->dest == node)
                        {
                            cout<<"Deleting edge ["<<edge->src->data<<"] -> ["<<node->data<<"] ..."<<endl;
                            this->edge_list.erase( this->edge_list.begin() + index);
                            index--;
                            edge->src->adjacency_degree--;
                            delete edge;
                            //delete node from the edge->src adjacent nodes list
                            for(int i= 0; i< edge->src->adjacent_nodes.size(); i++)
                            {
                                if( node == edge->src->adjacent_nodes[i])
                                {
                                    edge->src->adjacent_nodes.erase(edge->src->adjacent_nodes.begin() + i);
                                }
                            }
                            
                        }
                        index++;
                    }
                    for(int i=0; i<this->vertex_list.size(); i++)
                    {
                        if(node == this->vertex_list[i])
                        {
                            cout<<"Deleting node with value "<<vertex_list[i]->data<<" ..."<<endl;
                            this->vertex_list.erase( this->vertex_list.begin() + i);
                            delete node;
                        }
                    }
                }
                else{
                    for(int i=0; i<this->vertex_list.size(); i++)
                    {
                        if(node == this->vertex_list[i])
                        {
                            cout<<"Deleting node with value "<<vertex_list[i]->data<<" ..."<<endl;
                            this->vertex_list.erase( this->vertex_list.begin() + i);
                            delete node;
                        }
                    }
                }
            }
            else cout<<"The node is not in the graph."<<endl;
        }
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
        void print_vertices()
        {
            for(Node *vertex : this->vertex_list)
            {
                cout<<"["<<vertex->data<<"] ";
            }
        }

        void print_edges()
        {
            for(Edge *edge : this->edge_list)
            {
                cout<<"["<<edge->src->data<<"] -> "<<"["<<edge->dest->data<<"] "<<endl;
            }
        }

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
            while(opc != 7)
            {
                system("cls");
                print("MENU");
                cout<<"Enter: "<<endl;
                cout<<"1 -> Add a vertex"<<endl;
                cout<<"2 -> Remove a vertex"<<endl;
                cout<<"3 -> Vertex degrees"<<endl;
                cout<<"4 -> Print the Graph"<<endl;
                cout<<"5 -> Print vertices list"<<endl;
                cout<<"6 -> Print edges list"<<endl;
                cout<<"7 -> Exit"<<endl;
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
                    int vertex_to_delete;
                    system("cls");
                    cout<<"Enter the vertex value to eliminate: ";
                    cin>>vertex_to_delete;
                    delete_vertex(vertex_to_delete);
                    system("pause");
                }
                else if (opc == 3)
                {
                    int vertex;
                    system("cls");
                    cout<<"Enter the vertex value: ";
                    cin>>vertex;
                    query_vertex(vertex,true);
                    system("pause");
                }
                else if (opc == 4)
                {
                    system("cls");
                    print_graph();
                    system("pause");
                }
                else if (opc == 5)
                {
                    system("cls");
                    print_vertices();
                    system("pause");
                }
                else if (opc == 6)
                {
                    system("cls");
                    print_edges();
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