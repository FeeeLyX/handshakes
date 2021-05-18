import vk
import networkx as nx

class VKGraphs:
  def __init__(self, token):
    self.session = vk.Session(token)
    self.vk_api = vk.API(self.session, v="5.130")
    self.graph = nx.Graph()

  def get_friends(self, id):
    response = self.vk_api.friends.get(user_id=id)
    return response['items']
  
  def get_sex(self, id):
    response = self.vk_api.users.get(user_id=id, fields='sex')
    return response[0]['sex']

  def add_fofs(self, id):
    start_id = id
    sex = self.get_sex(id)
    color = 'magenta' if sex == 1 else 'cyan' 
    self.graph.add_node(start_id, color=color)

    friends = self.get_friends(start_id)
    for friend in friends:
      if not self.graph.has_node(friend):
        sex = self.get_sex(friend)
        color = 'magenta' if sex == 1 else 'cyan' 
        self.graph.add_node(friend, color=color)
      self.graph.add_edge(start_id, friend)
      try:
        fofs = self.get_friends(friend)
        for fof in fofs:
          if self.graph.has_node(fof):
            self.graph.add_edge(friend, fof)
      except Exception as e:
        print(e)
  
  def add_person(self, id):
    if not id in self.graph:
      try:
        friends = self.get_friends(id)
        sex = self.get_sex(id)
        color = 'magenta' if sex == 1 else 'cyan'
        self.graph.add_node(id, color=color)

        for friend in friends:
          if friend in self.graph:
            self.graph.add_edge(id, friend)
      except Exception as e:
        print(e)

  def visualize(self, wl):
    colors = []
    for node in self.graph:
      colors.append(self.graph.nodes[node]['color'])
    nx.draw_spring(self.graph,
                   node_color = colors,
                   with_labels=wl)

if __name__ == "__main__":
  # get API token
  f = open("token.txt", "r")
  token = f.readline()
  f.close()
  
  # test
  v = VKGraphs(token)
  v.add_fofs(51166239)
  v.visualize(wl=False)
