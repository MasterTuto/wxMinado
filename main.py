import random
import wx

class CampoMinado(wx.Frame):
	numeroDeBombas = 2
	alturaTabuleiro = 10
	larguraTabuleiro = 10

	alturaTabuleiroTemp = numeroDeBombas
	larguraTabuleiroTemp = alturaTabuleiro
	numeroDeBombasTemp = larguraTabuleiro

	def __init__(self, *args, **kwargs):
		wx.Frame.__init__(self, *args, **kwargs)

		self.sizerPrincipal = wx.BoxSizer(wx.VERTICAL)
		boxTitulos = wx.BoxSizer(wx.HORIZONTAL)
		boxConfiguracoes = wx.BoxSizer(wx.HORIZONTAL)

		self.painel = wx.Panel(self)
		self.painel.SetBackgroundColour(wx.Colour(255,255,255))

		self.botoes = []
		self.bombas = []
		self.numeroBombasRestantes = self.numeroDeBombas
		self.bombasMarcadas = {}
		self.botoesLivres = {}


		bombasRestantesStatic = wx.StaticText(self.painel, label="Bombas livres: ")
		self.bombasRestantes = wx.StaticText(self.painel, label=str(self.numeroBombasRestantes))

		boxTitulos.Add(bombasRestantesStatic, 0, wx.EXPAND | wx.ALL | wx.CENTRE, 3)
		boxTitulos.Add(self.bombasRestantes, 0, wx.EXPAND | wx.ALL | wx.CENTRE, 3)

		self.sizerPrincipal.Add(boxTitulos)

		self.boxTabuleiro = self.gerarPainelTabuleiro()

		numeroDeLinhasStatic = wx.StaticText(self.painel, label="Nº de Linhas: ")
		self.numeroDeLinhas = wx.TextCtrl(self.painel, size=(30, -1))

		numeroDeColunasStatic = wx.StaticText(self.painel, label="Nº de colunas: ")
		self.numeroDeColunas = wx.TextCtrl(self.painel, size=(30, -1))

		numeroDeBombasStatic = wx.StaticText(self.painel, label="Nº de bombas: ")
		self.txtNumeroDeBombas = wx.TextCtrl(self.painel, size=(30, -1))

		botaoAplicar = wx.Button(self.painel, label="Aplicar")
		botaoResetar = wx.Button(self.painel, label="Resetar")

		botaoAplicar.Bind(wx.EVT_BUTTON, self.aplicarMudancas)
		botaoResetar.Bind(wx.EVT_BUTTON, self.resetarJogo)

		boxConfiguracoes.Add(numeroDeLinhasStatic, 0, wx.ALL, 2)
		boxConfiguracoes.Add(self.numeroDeLinhas, 1, wx.ALL, 2)
		boxConfiguracoes.Add(numeroDeColunasStatic, 0, wx.ALL, 2)
		boxConfiguracoes.Add(self.numeroDeColunas, 1, wx.ALL, 2)
		boxConfiguracoes.Add(numeroDeBombasStatic, 0, wx.ALL, 2)
		boxConfiguracoes.Add(self.txtNumeroDeBombas, 1, wx.ALL, 2)
		boxConfiguracoes.Add(botaoAplicar, 0, wx.ALL, 2)
		boxConfiguracoes.Add(botaoResetar, 0, wx.ALL, 2)

		self.sizerPrincipal.Add(self.boxTabuleiro, 1, wx.ALL | wx.EXPAND, 2)
		self.sizerPrincipal.Add(boxConfiguracoes, 0, wx.ALL, 3)

		self.sortearBombas()

		self.painel.SetSizer(self.sizerPrincipal)
		self.sizerPrincipal.Fit(self.painel)
		self.painel.SetAutoLayout(1)
		self.Show()


	def gerarPainelTabuleiro(self):
		painel = wx.Panel(self.painel)
		painel.SetBackgroundColour(wx.Colour(255, 255, 255))

		boxTabuleiro = wx.BoxSizer(wx.VERTICAL)

		for i in range(self.alturaTabuleiro):
			self.botoes.append([])
			self.bombas.append([])
			sizerTemp = wx.BoxSizer(wx.HORIZONTAL)
			for j in range(self.larguraTabuleiro):
				bmp = wx.Bitmap()

				botaoTemp = wx.Button(painel, label="", size=(30,30), style=wx.NO_BORDER)
				botaoTemp.SetBackgroundColour(wx.Colour(255, 255, 255))
				botaoTemp.SetFont( wx.Font( wx.FontInfo(20).Bold().FaceName('Impact') ) )
				botaoTemp.SetBitmap(bmp)
				
				self.botoes[i].append(botaoTemp)
				self.bombas[i].append(False)

				self.bombasMarcadas[botaoTemp] = False
				self.botoesLivres[botaoTemp] = False
				
				sizerTemp.Add(botaoTemp,1,wx.EXPAND |wx.ALL, 3)
				sizerTemp.Add(wx.StaticLine(painel, style=wx.VERTICAL),0,wx.EXPAND)

				botaoTemp.Bind(wx.EVT_BUTTON, self.checarBombas)
				botaoTemp.Bind(wx.EVT_ENTER_WINDOW, self.botaoHover)
				botaoTemp.Bind(wx.EVT_LEAVE_WINDOW, self.botaoOut)
				botaoTemp.Bind(wx.EVT_RIGHT_DOWN, self.marcarBomba)

			boxTabuleiro.Add(sizerTemp,1,wx.EXPAND)
			boxTabuleiro.Add(wx.StaticLine(painel, style=wx.HORIZONTAL),0,wx.EXPAND)

		painel.SetSizer(boxTabuleiro)

		return painel

	def resetarJogo(self, event):
		self.sizerPrincipal.Detach(self.boxTabuleiro)
		self.boxTabuleiro.Destroy()
		
		self.alturaTabuleiro = self.alturaTabuleiroTemp
		self.larguraTabuleiro = self.larguraTabuleiroTemp
		self.numeroDeBombas = self.numeroDeBombasTemp

		self.botoes = []
		self.bombas = []
		self.numeroBombasRestantes = self.numeroDeBombas
		self.bombasMarcadas = {}
		self.botoesLivres = {}

		self.boxTabuleiro = self.gerarPainelTabuleiro()
		self.sortearBombas()

		self.bombasRestantes.SetLabel(str(self.numeroDeBombas))
		
		self.sizerPrincipal.Insert(1, self.boxTabuleiro, 1, wx.EXPAND)
		self.sizerPrincipal.Layout()


	def aplicarMudancas(self, event):
		self.alturaTabuleiroTemp = int(self.numeroDeLinhas.GetValue())
		self.larguraTabuleiroTemp = int(self.numeroDeColunas.GetValue())
		self.numeroDeBombasTemp = int(self.txtNumeroDeBombas.GetValue())

		if (self.numeroDeBombasTemp > self.alturaTabuleiroTemp*self.larguraTabuleiroTemp):
			event.Skip()
			wx.MessageDialog(self.painel, message="Insira um valor menor que o numero de células!", style=wx.ICON_ERROR).ShowModal()

			self.alturaTabuleiroTemp = self.alturaTabuleiro
			self.larguraTabuleiroTemp = self.larguraTabuleiro
			self.numeroDeBombasTemp = self.numeroDeBombas
			return

		

	def marcarBomba(self, event):
		botao = event.GetEventObject()
		if (self.numeroBombasRestantes == 0): event.Skip();return

		if not (self.bombasMarcadas[botao]):
			self.numeroBombasRestantes -= 1
			self.bombasRestantes.SetLabel(str(self.numeroBombasRestantes))
			botao.SetBackgroundColour(wx.Colour(255,30,30))
			self.bombasMarcadas[botao] = True
		else:
			self.numeroBombasRestantes += 1
			self.bombasRestantes.SetLabel(str(self.numeroBombasRestantes))
			botao.SetBackgroundColour(wx.Colour(255,255,255))

			self.bombasMarcadas[botao] = False


	def botaoOut(self, event):
		item = event.GetEventObject()
		corAtual = item.GetBackgroundColour() 
		if not(self.botoesLivres[item]) and corAtual != wx.Colour(255,30,30): item.SetBackgroundColour(wx.Colour(255, 255, 255))
	
	def botaoHover(self, event):
		item = event.GetEventObject()
		self.beforeColour = item.GetBackgroundColour()
		corAtual = item.GetBackgroundColour() 
		if not(self.botoesLivres[item]) and corAtual != wx.Colour(255,30,30): item.SetBackgroundColour(wx.Colour(0, 0, 0))

	def obterVizinhosBombas(self, i, j):
		total = 0
		vizinhosPosicoes = [(-1, -1), (-1, 0), (-1, 1), (0,-1), (0,1), (1, -1), (1, 0), (1, 1)]
		vizinhos = []
		for posicao in vizinhosPosicoes:
			ni = i+posicao[0]
			nj = j+posicao[1]
			if (ni >= 0 and nj >= 0 and ni < len(self.botoes) and nj < len(self.botoes[0]) and self.bombas[ni][nj]):
				vizinhos.append((ni, nj))
		return vizinhos

	def mostrarBombas(self):
		for i in range(self.alturaTabuleiro):
			for j in range(self.larguraTabuleiro):
				if self.bombas[i][j]:
					bmpDisabled = wx.Bitmap('exploded.png')
					self.botoes[i][j].SetBitmapDisabled(bmpDisabled)

	def liberarBombas(self, i, j, processados=set()):
		vizinhosBombas = self.obterVizinhosBombas(i, j)

		vizinhosPosicoes = [(-1, -1), (-1, 0), (-1, 1), (0,-1), (0,1), (1, -1), (1, 0), (1, 1)]
		
		numeroVizinhosBombas = len(vizinhosBombas)

		if (numeroVizinhosBombas == 0):
			for vizinho in vizinhosPosicoes:
				ni = i+vizinho[0]
				nj = j+vizinho[1]
				if (ni >= 0 and nj >= 0 and ni < len(self.botoes) and nj < len(self.botoes[0]) and not(self.bombas[ni][nj]) and (ni, nj) not in processados):
					processados.add((ni, nj))
					self.liberarBombas(ni, nj, processados)

		if (i >= 0 and j >= 0 and i < len(self.botoes) and j < len(self.botoes[0]) and numeroVizinhosBombas != 0):
			if numeroVizinhosBombas <= 2:
				self.botoes[i][j].SetForegroundColour(wx.Colour(255,246,0))
			elif numeroVizinhosBombas <= 4:
				self.botoes[i][j].SetForegroundColour(wx.Colour(255,195,2))
			elif numeroVizinhosBombas <= 6:
				self.botoes[i][j].SetForegroundColour(wx.Colour(255,143,0))
			else:
				self.botoes[i][j].SetForegroundColour(wx.Colour(255,5,5))
			
			self.botoes[i][j].SetLabel(str(numeroVizinhosBombas))
		
		
		self.botoesLivres[self.botoes[i][j]] = True
		self.botoes[i][j].SetBackgroundColour(wx.Colour(150, 150, 150))

	def verificarVitoria(self, botao):
		botoesLivres = 0
		for i in range(self.alturaTabuleiro):
			for j in range(self.larguraTabuleiro):
				if not(self.botoesLivres[self.botoes[i][j]]):
					botoesLivres += 1

		if (botoesLivres == self.numeroDeBombas):
			return True
		else:
			return False

	def bloquearBotoes(self):
		for i in range(self.alturaTabuleiro):
			for j in range(self.larguraTabuleiro):
				self.botoes[i][j].Disable()
		self.mostrarBombas()
	
	def checarBombas(self, event):
		botao = event.GetEventObject()
		if(self.bombasMarcadas[botao]): event.Skip(); return
		i, j = [(i, self.botoes[i].index(botao)) for i in range(self.alturaTabuleiro) if botao in self.botoes[i]][0]

		if (self.bombas[i][j]):
			wx.MessageDialog(self, message="PERDEU MLK KKKKKKKKKKKjjjjj", style=wx.ICON_INFORMATION).ShowModal()
			fimDoJogo = True
			self.mostrarBombas()
			self.bloquearBotoes()
		else:
			self.liberarBombas(i, j)

		vitoria = self.verificarVitoria(botao)
		
		if vitoria:
			wx.MessageDialog(self, message="GANHOU hein, fdp...", style=wx.ICON_INFORMATION).ShowModal()
			self.bloquearBotoes()

	def sortearBombas(self):
		for k in range(self.numeroDeBombas):
			i = random.randrange(0,self.alturaTabuleiro)
			j = random.randrange(0,self.larguraTabuleiro)

			while (self.bombas[i][j] == True):
				i = random.randrange(0,self.alturaTabuleiro)
				j = random.randrange(0,self.larguraTabuleiro)

			self.bombas[i][j]=True


app = wx.App(False)
CampoMinado(parent=None, size=(400,400))
app.MainLoop()