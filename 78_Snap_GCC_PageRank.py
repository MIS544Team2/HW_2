import pandas as pd
import json
import numpy as np
#-import sanp-stanford graph analysis package
import snap

#---Load the merged graph exported in Q4
with open('merged-graph.json') as f:
	data=json.load(f)
#---Covert the graph structure for SNAP
#-Convert the graph data as DataFrame and assign column names
df =pd.DataFrame(data.items(), columns=['Ego_Name','Followers_Name'])

#-Give each user name a pseudo id
df_id_lite=pd.DataFrame()
df_id_lite['Ego_Name']=Verts
df_id_lite['Ego_ID']=df_id_lite.index
#-Create the User Name and ID mapping file
df_id_lite.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/name_pseudoID_mapping.txt', header=None, index=None, sep=' ', mode='a')

#-Create int edges file for SNAP
add_ego_pseudoid=pd.merge(df, df_id_lite, how='left', on=['Ego_Name'])
df_iter2=add_ego_pseudoid.explode('Followers_Name')
df_iter2.dropna(subset = ["Followers_Name"], inplace=True)

add_follower_pseudoid=pd.merge(df_iter2, df_id_lite.rename(columns={'Ego_Name':"Followers_Name",'Ego_ID':'Follower_ID'}), how='left', on=['Followers_Name'])
add_follower_pseudoid.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/full_data_pseudo.txt', header=None, index=None, sep=' ', mode='a')

#-Save the graph file for SNAP
subset2 = add_follower_pseudoid[['Ego_ID','Follower_ID']]
subset2.to_csv('/mnt/c/Users/leona/Documents/Leona_Python/MIS544_Team_repo/hw2/HW_2/graph_lite.txt', header=None, index=None, sep=' ', mode='a')


# Edges= [tuple(x) for x in subset.to_numpy()]

#------------------------------------------------------------
#---Q7 Compute the Global Clustering Coef using SNAP package
#------------------------------------------------------------
#-Create a TUNGraph: undirected graph (single edge between an unordered pair of nodes)
UGraph = snap.LoadEdgeList(snap.PUNGraph, "graph_lite.txt", 0, 1)
# UGraph.Dump()

#-Create globale clustering coef computation function
#-Such clustering coefficients were defined by Watts and Strogatz in 1999, before another version of "global clustering coefficient" was considered - not an average of clustering coefficients for each node, but just 3*(number of triangles)/(number of triplets)
def clustering_coef(G , mode_for_end_nodes = 'put_zeros' ):
    '''
    Calculate vector of clustering coefficient for each node 
    G is an undirected Graph 
    mode_for_end_nodes = 'nan' - end/disconnected nodes will be ignored i.e. non included in output list
    mode_for_end_nodes = 'put_zero' - assign zero for end/disconnected
    
    list_clusterning_coefs_allnodes = clustering_coef(UGraph)
    https://www.kaggle.com/alexandervc/hw1-ac/notebook
    '''
    list_clusterning_coefs_allnodes = []
    for n in G.Nodes():
        NodeVec = snap.TIntV()
        snap.GetNodesAtHop(G, n.GetId(), 1, NodeVec, False) # Get neigbours of current node 
        current_degree = len(NodeVec) # same as n.GetDeg()
        if current_degree <= 1: # skip disconnected&end nodes - impossible to calculate for them - getting division by zero
            if mode_for_end_nodes == 'nan':
                continue 
            else:
                list_clusterning_coefs_allnodes.append(0)
                continue
        count_edges_between_neigbours = 0
        for neigbor1 in NodeVec:
            for neigbor2 in NodeVec:
                if neigbor1 >= neigbor2:
                    continue
            if G.IsEdge(neigbor1, neigbor2):
                count_edges_between_neigbours += 1
        clustering_coef_current_node = 2*count_edges_between_neigbours/ (current_degree * (current_degree-1)  )
        list_clusterning_coefs_allnodes.append(clustering_coef_current_node)
    return list_clusterning_coefs_allnodes


list_clusterning_coefs_allnodes = clustering_coef(UGraph, mode_for_end_nodes = 'put_zeros' )
list_clusterning_coefs_allnodes

gcc=np.mean(list_clusterning_coefs_allnodes)
lcc=snap.GetClustCf(UGraph)


NI = UGraph.Nodes()
NId = NI.GetId()
GroupSet = snap.TIntSet()
for NbrIdx in range(4):
    GroupSet.AddKey(NI.GetOutNId(NbrIdx))

#-Compute another Global Clustering Coef - Transitivity   
#triads = snap.GetNodeTriadsAll(UGraph, NId)
#closed_triads_num=triads[0]
#open_triads_num=triads[2]
#transitivity = 3*closed_triads_num/open_triads_num


print("----------------------------------------------------------\n-------------Clustering Coef Result------------------\n----------------------------------------------------------\n Global Clustering Coef(Average all nodes' LocalCC):", gcc,"\n Built-in Local Clustering Coef:", lcc)


#------------------------------------------------------------
#---Q8 Compute the Global Clustering Coef using SNAP package
#------------------------------------------------------------

PRankH = snap.TIntFltH()
snap.GetPageRank(UGraph, PRankH)
#-Compute page ranking score for each node
prank_scores=pd.DataFrame()
ids=[]
scores=[]
for item in PRankH:
    ids.append(item)
    scores.append(PRankH[item])
    
prank_scores["Node_ID"]=ids
prank_scores["Page_Rank_Score"]=scores
col_names=["Node_Name","Node_ID"]

#-Merge the user name
data=pd.read_csv('name_pseudoID_mapping.txt', header=None, names=col_names, delimiter=' ')
prank_scores_w_Name=pd.merge(prank_scores, data, how='left', on=['Node_ID'])

#-Sort the list and print out top 10
rank_list= prank_scores_w_Name.sort_values(by=["Page_Rank_Score"], ascending=False, ignore_index=True)
top10=rank_list.head(n=10)
top10.to_csv('top_10.txt', header=None, index=None, sep=' ', mode='a')
print("----- Top 10 nodes with their PageRank scores -----\n", top10)
