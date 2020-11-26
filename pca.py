#This file is mainly used to generate cool screenshots for presentations
#It also implements PCA and Clustering
import pandas as pd
import numpy as np

from mpl_toolkits.mplot3d import Axes3D  # noqa: F401 unused import
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

from sklearn.decomposition import PCA
from sklearn.cluster import SpectralClustering

from db import getMarkedMinutes, FIELDS_IN_ORDER, actIDToName



#Dataframe headers
namedFields = FIELDS_IN_ORDER.split(', ')+['answer']

#Data, correct answers
a, b = getMarkedMinutes()

#Convert activity IDs to activity names
#A dictionary is used to avoid unnecessary database requests
b1 = set([x[0] for x in b])
b2 = {x:actIDToName(x) for x in b1}
b3 = [b2[x[0]] for x in b]

#Convert to dataframe
d = [a[i]+(b3[i],) for i in range(len(a))]
df = pd.DataFrame(data=d, columns=namedFields)

del b1, b2, b3, d

print(df)
input()

plt.style.use('dark_background')

pca = PCA(n_components=3)
pt = pca.fit_transform(a)

print('variance', pca.explained_variance_ratio_)
print('eigenvalues?', pca.singular_values_)

#Set to true this if you're using the SankeyMATIC
if False:
	vrat = pca.explained_variance_ratio_
	vectors = pca.components_
	for ii, v in enumerate(vectors):
		print('####')
		
		for kkk in range(1):
			vv = 0
			vvv = []
			for i, value in enumerate(v):
				print(f'{namedFields[i]} [{abs(value*vrat[ii]):.5f}] PC{ii}')


df = pd.DataFrame(data=pt, columns=['PC1', 'PC2', 'PC3'])
print(df)
input()


#Diagram after PCA
colors = ['', 'r', 'g', 'b', 'yellow']
plt.scatter([x[0] for x in pt], [x[1] for x in pt], c=[colors[x[0]] for x in b])
plt.legend(handles = [mpatches.Patch(color=colors[x], label=['', 'A', 'B', 'C', 'D'][x]) for x in range(1, 5)])
plt.show()


#Diagram after Clustering, 3D
clustering = SpectralClustering(n_clusters=4, random_state=0).fit_predict(pt)
print(clustering)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter([x[0] for x in pt], [x[1] for x in pt], [x[2] for x in pt], c=[colors[x+1] for x in clustering])
plt.show()
