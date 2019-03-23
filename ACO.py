import numpy as np, time, csv
from numpy import inf
import matplotlib.pyplot as plt
start_time = time.time()
np.seterr(divide='ignore', invalid='ignore')

#Reading Statistics File, 
reader = csv.reader(open("Statistics3.csv", "r"))
x = list(reader)
dis = np.array(x).astype('int64')


# intialization part
iteration = 100
no_ants = len(dis)             	#no. of Ants
no_cities = len(dis)            #no. of Cities
e = .5           				#evaporation rate
alpha = 1           			#Alpha rate
beta = 2
min_cost = 100000

visibility = 1/dis     #visibility Matrix : Visibility(i,j) = 1/dis[i,j]
visibility[visibility == inf ] = 0


#intializing pheromone with 1 for all links
pheromone = 1*np.ones((no_cities,no_cities))

#intializing route for all ants
route = np.ones((no_ants,no_cities+1))


##***************************Iterations starts from here*******************************
for ite in range(iteration):
    route[:,0] = 1         								#Starting Position i.e. city no. 1
    for i in range(no_ants):
        temp_visibility = np.array(visibility)         #creating a copy of visibility
      
        for j in range(no_cities-2):    
            cur_loc = int(route[i,j]-1)       			#current city of the ant
            
            temp_visibility[:,cur_loc] = 0     #update visibility of the current city as zero
            
            pher_matrix = np.multiply(pheromone[cur_loc,:], alpha)        #calculating pheromone
            visibility_matrix = np.multiply(temp_visibility[cur_loc,:], beta)  #calculating visibility
            
            pher_matrix = pher_matrix[:,np.newaxis]                    
            visibility_matrix = visibility_matrix[:,np.newaxis]
            
            combine_array = np.zeros(no_cities)     #intializing Combine array of Pheromone & Visibility to 0
            cum_prob = np.zeros(no_cities)            #intializing cummulative probability array to 0
            
            combine_array = np.multiply(pher_matrix,visibility_matrix)     #calculating the  (Pheromone * Visibility)
                        
            total = np.sum(combine_array)                        #summation of (Pheromone * Visibility) of all links 
            
            prob = combine_array/total                           #probability of each link
            
            cum_prob = np.cumsum(prob)                           #cummulative sum of probability
            cum_prob[np.isnan(cum_prob)] = 1
            r = np.random.random_sample()                        #generate a randon no. r between 0 to 1
            city = np.nonzero(cum_prob>r)[0][0]+1                #select the next city having probability > r 
            
            route[i,j+1] = city                                  #adding city to route 
            
        left = list(set([i for i in range(1,no_cities+1)])-set(route[i,:-2]))[0]     #finding the last untraversed city to route
        route[i,-2] = left                   					 #adding untraversed city to route
           
    route_optimum = np.array(route)              				 #intializing optimum route array
    distance_cost = np.zeros((no_ants,1))          		   #intializing total tour distance for each ant to 0
    
    for i in range(no_ants):
        summation = 0
        for j in range(no_cities-1):
            summation = summation + dis[int(route_optimum[i,j])-1,int(route_optimum[i,j+1])-1]   #calcualting total distance by an ant
        distance_cost[i] = summation                              #Additon Total distance of each ant
    min_loc = np.argmin(distance_cost)             #finding minimum location from distance_cost matrix
    if(min_cost > distance_cost[min_loc]): 
        min_cost = distance_cost[min_loc]              #Finding path distance using min_loc
    best_route = route[min_loc,:]                  #intializing current traversed as best route
    pheromone = (1-e)*pheromone                    #evaporate pheromone
    for i in range(no_ants):
        for j in range(no_cities-1):
            dt = 1/distance_cost[i]
            pheromone[int(route_optimum[i,j])-1,int(route_optimum[i,j+1])-1] = pheromone[int(route_optimum[i,j])-1,int(route_optimum[i,j+1])-1] + dt   
            #updating the pheromone with delta_distance i.e. 1/total_distance of tour of an ant
print('path at the end :', route)	#path of all ant at end
print('best path :',best_route)		#best path
print('cost of the best path',int(min_cost[0]) + dis[int(best_route[-2])-1,0])    #min cost of path + distance to come back to starting city
print("--- total time taken == %s seconds ---" % (time.time() - start_time))
            
            
