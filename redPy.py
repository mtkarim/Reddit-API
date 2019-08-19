# Name(s): Mubasshir Karim, Connor Shannon
# WSU ID(s): G498M939, A353Q453
# File: redPy.py
# Assignment: Project
# Description: Filter a reddit search based on 'hot' section
# of search's scores (up/down votes) and number of comments,
# then sort them in order from least to greatest, uses the
# retrieved scores to store in a BST then prints it using API,
# and then a manual implementation of BST is done and displayed;
# all of this is gathered from initial user input. 

from abc import ABC, abstractmethod     # in-built python module
from binarytree import build, Node      # created python module
import collections                      # in-built python module
import dash                             # created modules
import dash_core_components as dcc      # created module
import dash_html_components as html     # created module
import praw                             # api created for reddit
import requests                         # created module
import requests.auth                    # created module

# start of user credentials

# client_auth = requests.auth.HTTPBasicAuth('APFPnUu-VVf6Qw', 'm_JJN47NFzF5CQfpF2uM_-3VgIM')
# post_data = {"grant_type": "password", "username": "cs400_python", "password": "datastructures123"}
# #headers = {"User-Agent": "bot /u/cs400_python"} #**
# headers = {"Authorization": "82038012465-iMfT8G0HCyqq_db7FW4pxKbyi-c", "User-Agent": "bot /u/cs400_python"}         # this "Authorization" changes each time code is ran
# response = requests.get("https://oauth.reddit.com/api/v1/me", headers=headers)
# #response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers) #**
# jsonHolder = response.json()
# #print(jsonHolder)

# # after pasting new authorization code, uncomment middle header + middle response 
# # and everthing below here until end of user credentials

# print("Username: "+ jsonHolder["name"])
# print("comment_karma: ")
# print(jsonHolder["comment_karma"])
# print("link_karma: ")
# print(jsonHolder["link_karma"])

# end of user credentials
  
# setting python reddit api wrapper (praw) to 'reddit'
# using specific credentials for client_id, client_search, 
# user_agent. All based off of the username and password. 
# Hence, each user has unique credentials.
reddit = praw.Reddit(client_id="APFPnUu-VVf6Qw",
                     client_secret="m_JJN47NFzF5CQfpF2uM_-3VgIM",
                     user_agent= "bot /u/cs400_python",
                     username="cs400_python",
                     password="datastructures123")

commentScore = {}       # based on number of comments
listScore = {}          # based on up/down votes
xbList = []             # list for 'before sorting'
ybList = []             # list for 'before sorting'
xaList = []             # list for 'after sorting'
yaList = []             # list for 'after sorting'
xcList = []             # list for 'comment section'
ycList = []             # list for 'comment section'

# RedditBase Class
class RedditBase():
    def __init__(self, para):
     self.para = para

    # helper function that generates 'data.tx' file 
    # and stores all the information in there
    def writeIntoFile(self, holderToWrite):
        file = open("data.txt", "a")
        lineDivider = ('------------------------')
        file.write(holderToWrite)
        file.write(lineDivider)

    # helper function used at the start of program
    def startReddit(self):
        # subRedditSearch = user input after prompt
        subRedditSearch = input ("\nWhat would you like to search for on Reddit? ")
        # subreddit = user input for search on reddit
        subreddit = reddit.subreddit(subRedditSearch)
        print("\nYou searched for :", subreddit.display_name)
        print("\nReddit's search result :", subreddit.title)
        self.writeIntoFile(subreddit.title)                         # stores title in data.txt
        print(subreddit.description)
        self.writeIntoFile(subreddit.description)                   # stores description in data.txt
        self.redditFiller(subreddit)                                # stores reddit search (user input) 
                                                                    # into redditFiller to get top 10 in 'hot'

    def redditFiller(self, subreddit):
        # for loop to get first 10 searches in 'hot' for reddit search
        for submission in subreddit.hot(limit=10):
            # gathers 10 posts based on 10 highest scores
            listScore[submission.score] = submission.title
            # gathers 10 posts based on 10 highest comments
            commentScore[submission.title] = submission.num_comments

        self.graphCreator(listScore)        # stores scores in graphCreator
        self.graphCreator1(commentScore)    # stores comments in graphCreator1

    # 'graphCreator' for search's scores before/after sorting
    def graphCreator(self, listScore):
        # before sorting
        print("\nBEFORE SORTING SCORES : ")                     # displays in terminal
        self.writeIntoFile("\n")
        self.writeIntoFile(" BEFORE SORTING SCORES ")           # stores in data.txt
        for k, v in listScore.items():                 
            print ("\nScore :", k, "\nTopic :", v) 
            xbList.append(k)                                                            # adds the values of scores to the xbList
            ybList.append(v)                                                            # adds the topics of respective scores to the ybList
            contentHolder = ('\n{} : {}\n'.format(k, v))                                # stores scores, topics in contentHolder
            self.writeIntoFile(contentHolder)                                           # contentHolder gets written into data.txt
            # summary for scores before sorting
            print("\nScores : ",xbList)                                                 # prints the scores before sorting list
            print("\nTopics : ",ybList)                                                 # prints the topics before sorting list
        # after sorting
        ods = collections.OrderedDict(sorted(listScore.items()))                        # od is for ordered diction which sets values in order from least to greatest
        print("\nAFTER SORTING SCORES : ")                                              # stores in terminal
        self.writeIntoFile(" AFTER SORTING SCORES ")                                    # stores in data.txt
        for k, v in ods.items():                                                       
            contentHolder = ('\n{} : {}\n'.format(k, v))
            self.writeIntoFile(contentHolder)                                           # stores content of topic/votes after sort in data.txt
            print ("\nScore :", k, "\nTopic :", v)                                      # prints topic/votes horizontally                    
            xaList.append(k)                                # concatenates/joins 
            yaList.append(v)                                # concatenates/joins
        # summary for scores after sorting
        print("\nSUMMARY FOR SCORES AFTER SORTING :")
        print("\nScores : ", xaList)             # prints concatenated list of scores after sorting complete
        print("\nTopics : ", yaList)             # prints concatenated list of topics after sorting complete

    # 'graphCreator1' for search's comment scores
    def graphCreator1(self, commentScore):
        # retreiving comments here
        print("\nCOMMENTS SECTION: ")                   # displays in terminal
        self.writeIntoFile(" COMMENTS SECTION ")        # stores in data.txt
        for k, v in commentScore.items():          
            print ("\nTopic :", k, "\nNumber of Comments :", v)
            xcList.append(k)
            ycList.append(v)
            contentHolder = ('\n{} : {}\n'.format(k, v))
            self.writeIntoFile(contentHolder)
        # summary for comments section
        print("\nSUMMARY FOR COMMENTS :")
        print("\nTopics : ", xcList)
        print("\nNumber of Comments : ", ycList)

# Node class 
class NodeTree:
    def __init__(self, getData):    # default constructor (__init__) 
        self.getLeft = None         # left child set to 'none' 
        self.getRight = None        # right child set to 'none' 
        self.getData = getData      

    # function 'insert', passes self and getData
    def insert(self, getData):     
        if getData < self.getData:
            if self.getLeft is None:
                self.getLeft = NodeTree(getData)
            else:
                self.getLeft.insert(getData)
        elif getData > self.getData:
            if self.getRight is None:
                self.getRight = NodeTree(getData)
            else:
                self.getRight.insert(getData)
        else:
            self.getData = getData

    # function printTree
    def printTree(self):                                        
        if self.getLeft:
            self.getLeft.printTree()
        print(self.getData)
        if self.getRight:
            self.getRight.printTree()

    # function for inorder
    # In-order:
    # 1-Traverse the left subtree.
    # 2-Visit root.
    # 3-Traverse the right subtree.
    def inorderTraversal(self,rootTree):                           
        res = []
        if rootTree:
            res = self.inorderTraversal(rootTree.getLeft)
            res.append(rootTree.getData)
            res = res + self.inorderTraversal(rootTree.getRight)
        return res

    # function for preorder
    # Pre-order:
    # 1-Visit the root.
    # 2-Traverse the left subtree.
    # 3-Traverse the right subtree.
    def preorderTraversal(self, rootTree):                         
        res = []
        if rootTree:
            res.append(rootTree.getData)
            res = res + self.preorderTraversal(rootTree.getLeft)
            res = res + self.preorderTraversal(rootTree.getRight)
        return res

    # function for postorder
    # Post-order:
    # 1-Traverse the left subtree.
    # 2-Traverse the right subtree.
    # 3-Visit the root.
    def postorderTraversal(self, rootTree):                        
        res = []
        if rootTree:
            res = self.postorderTraversal(rootTree.getLeft)
            res = res + self.postorderTraversal(rootTree.getRight)
            res.append(rootTree.getData)
        return res

    # function to invert the BST
    def invertTree(self, rootTree):                                
        if rootTree is None:
            return None
        rootTree.left, rootTree.right = rootTree.right, rootTree.left
        self.invertTree(rootTree.left)
        self.invertTree(rootTree.right)
        return rootTree

# DashBase Class
class DashBase(ABC):            # ABC is python module that stands for abstract base class - in built tools
    def __init__(self, par):    # default constructor
        self.par = par

    # imported from ABC module
    @abstractmethod
    def chartsTime(self, param1, param2, param3, param4, param5, param6):
        raise NotImplementedError("Subclass must implement this abstract method")

# DashBoard Class
class DashBoard(DashBase):
    def __init__(self, f):
        super().__init__(f)

    # chartsTime is weblink graphs of results
    def chartsTime(self, xcList, ycList, xaList, yaList, xbList, ybList):
        graphy = dash.Dash()
        graphy.layout = html.Div([
            html.H1(
                children='Reddit Submissions (x-axis) v. Top Score & No. of Comments(y-axis)',  # title of webpage
                style={
                    'textAlign': 'center',      # alignment of title
                }
            ),
            html.Div(                   # first layer of html for 'row'
                className="row",
                children=[              # child of 'row' is another html called 'six columns'
                    html.Div(
                        className="six columns",
                        children=[
                            html.Div(
                                dcc.Graph(              # dash module syntax to make class called graph
                                    id='right-graph',   # id for the graph class for comments
                                    figure={
                                        'data': [{
                                            'x': xcList,            # number of comments data used here
                                            'y': ycList,            # topic of comments data used here
                                            'type': 'scatter',      # using a scatter graph
                                            'name': 'Submissions v. Number of Comments'
                                        }],
                                        'layout': {     # height
                                            'height': 800,
                                        },
                                        'marker': {     # size and width
                                             'size': 15,
                                             'line': {'width': 0.5, 'color': 'red'}
                                        },
                                    }
                                )
                            )
                        ]
                    ),
                    html.Div(                           # html is built in dash module
                        className="six columns",
                        children=html.Div([
                            dcc.Graph(                  # dash core components built in
                                id='right-top-graph',   # id for graph before scores are sorted
                                figure={
                                    'data': [{
                                        'x': ybList,    # topics for search before sorted
                                        'y': xbList,    # up/down votes for search before sorted
                                        'type': 'bar',  # bar graph
                                        'name': 'Score v. Submissions'  # name 

                                    }],
                                    'layout': {         # formatting layout
                                        'height': 400,
                                        'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
                                        'legend':{'x': 0, 'y': 1},
                                        'hovermode':'closest'


                                    }
                                }
                            ),
                            dcc.Graph(                      # dash core components built in
                                id='right-bottom-graph',    # graph for after sorting
                                figure={
                                    'data': [{
                                        'x': yaList,    # topics of search after sort
                                        'y': xaList,    # up/down votes for search after sort
                                        'type': 'bar'   # bar graph
                                    }],
                                    'layout': {
                                        'height': 400,
                                        'margin': {'l': 40, 'b': 40, 't': 10, 'r': 10},
                                        'legend':{'x': 0, 'y': 1},
                                        'hovermode':'closest'
                                    }
                                }
                            ),

                        ])
                    )
                ]
            )
        ])

        # this is the url to view the graphs
        print("Here's a link to view your graphs: ")
        graphy.css.append_css({
            'external_url': 'https://codepen.io/chriddyp/pen/bWLwgP.css'
        })

        graphy.run_server(debug=True)

# 'main' for python
if __name__ == "__main__":
    # starts of program with 'redditStart' 
    # which asks for user input after prompt
    redditStart = RedditBase("redditStart")
    redditStart.startReddit()                              
    print("\nBinary Tree With Sorted List")             # 'build' is apart of the binarytree module and
    xaRoot = build(xaList)                              # build a tree with given values, in this case    
    print(xaRoot)                                       # the after sorted list                                                
    print("Manual Implementation of Binary Tree")       
    x = xaList[0]                                       # list for scores before sorting used
    rootTree = NodeTree(x)
    for valLoad in xaList:                              # for loop inserts values from after sorted list into rootTree
        rootTree.insert(valLoad)
    print("Printing Tree")
    print(rootTree.printTree())                         # prints rootTree which has after sorted list stored
    print("\nInOrder : Left -> Root -> Right")
    print(rootTree.inorderTraversal(rootTree))          # in order printed
    print("\nPreOrder : Root -> Left -> Right")
    print(rootTree.preorderTraversal(rootTree))         # pre order printed
    print("\nPostOrder : Left -> Right -> Root ")
    print(rootTree.postorderTraversal(rootTree), "\n")  # post order printed
    dashB = DashBoard("dashB")                          # puts results in order and creats graphs
    dashB.chartsTime(xcList, ycList, xaList, yaList, xbList, ybList)