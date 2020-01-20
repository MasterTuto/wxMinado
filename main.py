import random
import wx

class CampoMinado(wx.Frame):
	def __init__(self, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)

		sizerPrincipal = wx.BoxSizer(wx.VERTICAL)

		painel = wx.Panel(self)
		painel.SetBackgroundColour(wx.Colour(255,255,255))

		self.botoes = []
		self.bombas = []
		self.processados = [[False for i in range(8)] for j in range(8)]

		for i in range(8):
			self.botoes.append([])
			self.bombas.append([])
			sizerTemp = wx.BoxSizer(wx.HORIZONTAL)
			for j in range(8):
				bmp = wx.Bitmap()

				botaoTemp = wx.Button(painel, label="", size=(30,30), style=wx.NO_BORDER)
				botaoTemp.SetBackgroundColour(wx.Colour(255, 255, 255))
				botaoTemp.SetBitmap(bmp)
				
				self.botoes[i].append(botaoTemp)
				self.bombas[i].append(False)
				
				sizerTemp.Add(botaoTemp,1,wx.EXPAND |wx.ALL, 3)
				sizerTemp.Add(wx.StaticLine(painel, style=wx.VERTICAL),0,wx.EXPAND)

				botaoTemp.Bind(wx.EVT_BUTTON, self.checarBombas)
				botaoTemp.Bind(wx.EVT_ENTER_WINDOW, self.botaoHover)
				botaoTemp.Bind(wx.EVT_LEAVE_WINDOW, self.botaoOut)

			sizerPrincipal.Add(sizerTemp,1,wx.EXPAND)
			sizerPrincipal.Add(wx.StaticLine(painel, style=wx.HORIZONTAL),0,wx.EXPAND)

		self.sortearBombas()

		painel.SetSizer(sizerPrincipal)
		sizerPrincipal.Fit(painel)
		painel.SetAutoLayout(1)
		self.Show()

	def botaoOut(self, event):
		item = event.GetEventObject()
		if item.GetBackgroundColour() != wx.Colour(150, 150, 150): item.SetBackgroundColour(wx.Colour(255, 255, 255))
	
	def botaoHover(self, event):
		item = event.GetEventObject()
		self.beforeColour = item.GetBackgroundColour()
		
		if item.GetBackgroundColour() != wx.Colour(150, 150, 150): item.SetBackgroundColour(wx.Colour(0, 0, 0))

	def obterVizinhosBombas(self, i, j):
		total = 0
		vizinhosPosicoes = [(-1, -1), (-1, 0), (-1, 1), (0,-1), (0,1), (1, -1), (1, 0), (1, 1)]
		vizinhos = []
		for posicao in vizinhosPosicoes:
			ni = i+posicao[0]
			nj = j+posicao[1]
			if (ni >= 0 and nj >= 0 and ni < len(self.botoes) and nj < len(self.botoes) and self.bombas[ni][nj]):
				vizinhos.append((ni, nj))
		return vizinhos


	def mostrarBombas(self):
		for i in range(8):
			for j in range(8):
				if self.bombas[i][j]:
					bmpDisabled = wx.Bitmap('exploded.png')
					self.botoes[i][j].SetBitmapDisabled(bmpDisabled)

	def liberarBombas(self, i, j, processados=set()):
		vizinhosBombas = self.obterVizinhosBombas(i, j)
		print(vizinhosBombas)

		vizinhosPosicoes = [(-1, -1), (-1, 0), (-1, 1), (0,-1), (0,1), (1, -1), (1, 0), (1, 1)]
		
		numeroVizinhosBombas = len(vizinhosBombas)

		if (numeroVizinhosBombas == 0):
			print('jasasd')
			for vizinho in vizinhosPosicoes:
				ni = i+vizinho[0]
				nj = j+vizinho[1]
				if (ni >= 0 and nj >= 0 and ni < 8 and nj < 8 and not(self.bombas[ni][nj]) and (ni, nj) not in processados):
					processados.add((ni, nj))
					self.liberarBombas(ni, nj, processados)

		if (i >= 0 and j >= 0 and i < len(self.botoes) and j < len(self.botoes) and numeroVizinhosBombas != 0):
			self.botoes[i][j].SetLabel(str(numeroVizinhosBombas))
		
		self.botoes[i][j].SetBackgroundColour(wx.Colour(150, 150, 150))


	def checarBombas(self, event):
		i, j = [(i, self.botoes[i].index(event.GetEventObject())) for i in range(8) if event.GetEventObject() in self.botoes[i]][0]

		self.liberarBombas(i, j)

		if (self.bombas[i][j]):
			wx.MessageDialog(self, message="EXPLOSAO!!!", style=wx.ICON_QUESTION).ShowModal()
			self.mostrarBombas()

	def sortearBombas(self):
		for k in range(10):
			i = random.randrange(0,8)
			j = random.randrange(0,8)

			while (self.bombas[i][j] == True):
				i = random.randrange(0,8)
				j = random.randrange(0,8)

			self.bombas[i][j]=True
		for i in range(8):
			for j in range(8):
				if self.bombas[i][j]==True: print("(%s, %s)"%(i, j),end=' ')
		print()



app = wx.App(False)
CampoMinado(parent=None, size=(400,400))
app.MainLoop()