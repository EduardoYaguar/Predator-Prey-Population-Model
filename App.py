import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np

class MyFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0,1,2,3), weight=1)

        self.cycles = 3000

        self.a_slider = customtkinter.CTkSlider(self, from_=0.01, to=0.1, number_of_steps=100, command=self.update_plot)
        self.a_slider.set(0.04)
        self.a_slider.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        self.a_label = customtkinter.CTkLabel(self, text="Prey intrinsic growth rate (a)")
        self.a_label.grid(row=1, column=1, padx=10, pady=10)

        self.b_slider = customtkinter.CTkSlider(self, from_=0.001, to=0.01, number_of_steps=100, command=self.update_plot)
        self.b_slider.set(0.003)
        self.b_slider.grid(row=2, column=0, sticky='ew', padx=10, pady=10)
        self.b_label = customtkinter.CTkLabel(self, text="per-capita attack rate of predators on prey (b)")
        self.b_label.grid(row=2, column=1, padx=10, pady=10)

        self.c_slider = customtkinter.CTkSlider(self, from_=0.001, to=0.05, number_of_steps=100, command=self.update_plot)
        self.c_slider.set(0.01)
        self.c_slider.grid(row=3, column=0, sticky='ew', padx=10, pady=10)
        self.c_label = customtkinter.CTkLabel(self, text="Predators natural deathrate (c)")
        self.c_label.grid(row=3, column=1, padx=10, pady=10)

        self.f_slider = customtkinter.CTkSlider(self, from_=0.01, to=0.1, number_of_steps=100, command=self.update_plot)
        self.f_slider.set(0.02)
        self.f_slider.grid(row=4, column=0, sticky='ew', padx=10, pady=10)
        self.f_label = customtkinter.CTkLabel(self, text="Conversion rate (f)")
        self.f_label.grid(row=4, column=1, padx=10, pady=10)

        self.figure = None
        self.update_plot()


    def update_plot(self, event=None):
        a = self.a_slider.get()
        b = self.b_slider.get()
        c = self.c_slider.get()
        f = self.f_slider.get()


        prey_initial = 50 #población inicial presas
        K = 1200 # capacidad de carga
        predator_initial = 20 # poblacion inicial predadores

        prey_population = [prey_initial]
        predator_population = [predator_initial]
        marker_size = 2

        def prey(n):
            prey_model = prey_population[n-1]
            predator_model = predator_population[n-1]
            return prey_model + a * prey_model * (1 - prey_model / K) - b * prey_model * predator_model
        def predator(n):
            prey_model = prey_population[n-1]
            predator_model = predator_population[n-1]
            return predator_model + f * b * prey_model * predator_model - c * predator_model
        
        def model(): 
            for i in range(1,self.cycles):
                prey_population.append(prey(i))
                predator_population.append(predator(i))
        prey_e = c / (b * f) #punto de equilibrio presas
        predator_e = (a / b) * (1 - prey_e / K) #punto de equilibrio predadores

        if self.figure:
            self.figure.clear()

        model()
        self.figure = plt.figure()

        plt.axhline(y=predator_e, color='red', linestyle='--')
        plt.axhline(y=prey_e, color='red', linestyle='--')

        plt.plot(np.arange(self.cycles), prey_population, label='Prey Population', markersize=marker_size)
        plt.plot(np.arange(self.cycles), predator_population, label='Predator Population', markersize=marker_size)

        plt.ylabel('Population')
        plt.xlabel('Cycles')
        plt.title('Predator and Prey Populations over Time')
        plt.legend()

        canvas = FigureCanvasTkAgg(self.figure, master=self)
        canvas.draw()
        canvas.get_tk_widget().grid(row=0, column=0, sticky='nsew')


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Predator And Prey Population model")
        self.geometry('1080x990')

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.MyFrame = MyFrame(self)
        self.MyFrame.grid(row=0, column=0, sticky='nsew')



app = App()
app.mainloop()