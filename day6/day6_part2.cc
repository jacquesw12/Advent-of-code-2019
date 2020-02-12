#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <istream>
#include <sstream>

// To compile this code on command line:
// g++ -std=c++14 day6_part2.cc

class Node 
{
  public:
    std::string name;
    Node* left;
    Node* right;
    int depth;

    Node();
    Node(std::string name_, int depth_) : name(name_), depth(depth_),
                              left(nullptr), 
                              right(nullptr){ }
    void printNode();
    void printTree();
    void setupTree(std::string name, std::vector<std::pair<std::string, std::string> >& raw_input);
    Node* insertNode(std::string name, int depth);
};

Node* Node::insertNode(const std::string name, int depth)
{
  if (!left) 
  {
    Node* newNode = new Node(name, depth);
    left = newNode;
    return newNode;
  }
  if(!right)
  {
    Node* newNode = new Node(name, depth);
    right = newNode; 
    return newNode;
  }
}

void Node::printNode() {
    std::cout << "Node " << name << " depth " << depth << std::endl;
}

void Node::printTree()
{
  printNode();
  if (left)
    left->printTree();
  if (right)
    right->printTree();
}

void Node::setupTree(std::string name, std::vector<std::pair<std::string, std::string> >& raw_input) 
{
  for (const auto& elt : raw_input)
  {
    if (elt.first == name) {
      Node * newNode = insertNode(elt.second, depth + 1);
      newNode->setupTree(elt.second, raw_input);
    }
  }
}

Node* findNode(Node* node, const std::string& searchedName)
{
  if (node) {
    if (node->name == searchedName) {
      return node;
    }
    else {
       Node* curNode = findNode(node->left, searchedName);
       if (curNode == nullptr)
         curNode = findNode(node->right, searchedName);
       return curNode;
    }
  }
  else
    return nullptr;
}

Node* findCommonAncestor(Node* node, const std::string& name1, const std::string& name2)
{
  if (!node)
    return nullptr;
  if (node->name == name1 || node->name == name2)
    return node;

  Node* left = findCommonAncestor(node->left, name1, name2);
  Node* right = findCommonAncestor(node->right, name1, name2);

  if (left && right)
    return node;

  if (left)
    return left;
  else
    return right;
}

std::pair<std::string, std::string> split(const std::string& s, char delimiter)
{
  std::pair<std::string, std::string> planets;
  std::string planet;
  std::istringstream inputStream(s);
  
  std::getline(inputStream, planet, delimiter);
  planets.first = planet;
  std::getline(inputStream, planet, delimiter);
  planets.second = planet;

  return planets;
}

int main() {
  std::ifstream inputFile("input.txt");
  if (!inputFile)
    std::cout << "Could not open input file." << std::endl;
  
  std::vector<std::pair<std::string, std::string> > raw_input;
  std::string line;
  
  while(std::getline(inputFile, line))
  {
    std::pair<std::string, std::string> planets = split(line, ')');
    raw_input.push_back(planets);
  }

  Node* root = new Node("COM", 0);
  root->setupTree("COM", raw_input);

  Node* youNode = findNode(root, "YOU");
  youNode->printNode();
  Node* sanNode = findNode(root, "SAN");
  sanNode->printNode();
  
  Node* LCA = findCommonAncestor(root, "YOU", "SAN");
  if(LCA)
    LCA->printNode();
  else
    std::cout << "no common ancestor" << std::endl;

  int amountOrbitTransfer =  (youNode->depth - LCA->depth) + (sanNode->depth - LCA->depth) - 2;
  std::cout << "Amount of transfers needed : " << amountOrbitTransfer << std::endl;
  return 0;
}
