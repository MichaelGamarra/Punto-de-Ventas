from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior




inventario = [ 
    {'codigo':'111','nombre':'Leche', 'precio':10.0, 'cantidad':5},
    {'codigo':'112','nombre':'Yogur', 'precio':8.0, 'cantidad':7}, 
    {'codigo':'113','nombre':'Queso', 'precio':15.0, 'cantidad':3}, 
    {'codigo':'114','nombre':'Mantequilla', 'precio':12.0, 'cantidad':6}, 
    {'codigo':'115','nombre':'Crema', 'precio':9.0, 'cantidad':4}, 
    {'codigo':'116','nombre':'Helado', 'precio':20.0, 'cantidad':2}, 
    {'codigo':'117','nombre':'Nata', 'precio':7.0, 'cantidad':8}, 
    {'codigo':'118','nombre':'Leche condensada', 'precio':14.0, 'cantidad':5}, 
    {'codigo':'119','nombre':'Leche de almendras', 'precio':11.0, 'cantidad':9}, 
    {'codigo':'120','nombre':'Leche de coco', 'precio':13.0, 'cantidad':7}, 
    {'codigo':'121','nombre':'Leche de soja', 'precio':10.0, 'cantidad':6} 
] 



class SelectableRecycleBoxLayout(FocusBehavior, LayoutSelectionBehavior,
                                 RecycleBoxLayout):
    ''' Adds selection and focus behaviour to the view. '''
    touch_deselect_last  = BooleanProperty(True)


class SelectableBoxLayout(RecycleDataViewBehavior, BoxLayout):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        self.ids['_hashtag'].text = str(1+index)
        self.ids['_articulo'].text = data['nombre'].capitalize()
        self.ids['_cantidad'].text = str(data['cantidad_carrito'])
        self.ids['_precio_por_articulo'].text = str("{:.2f}".format(data['precio']))
        self.ids['_precio'].text = str("{:.2f}".format(data['precio_total']))
        return super(SelectableBoxLayout, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableBoxLayout, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)


    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0} y {1}".format(rv.data[index], 22))
        else:
            print("selection removed for {0}".format(rv.data[index]))



class RV(RecycleView):
    def __init__(self, **kwargs):
        super(RV, self).__init__(**kwargs)
        self.data = []
    
    def agregar_articulo(self,articulo):
        articulo['seleccionado'] = False
        indice = -1
        if self.data:
            for i in range(len(self.data)):
                if articulo['codigo']==self.data[i]['codigo']:
                    indice = i
            if indice >= 0:
                self.data[indice]['cantidad_carrito']+=1
                self.data[indice]['precio_total']=self.data[indice]['precio']*self.data[indice]['cantidad_carrito']
                self.refresh_from_data()
            else:
                self.data.append(articulo)
        else:
            self.data.append(articulo)






class VentasWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.total= 0.0

    def admin(self):
        print("Admin Presionado")
    
    def signout(self):
        print("signout Presionado")

    def eliminar_producto(self):
        print("Eliminar_Producto Seleccionado")

    def modificar_producto(self):
        print("Modificar_Producto Seleccionado")

    def agregar_producto_codigo(self, codigo):
        for producto in inventario:
            if codigo == producto['codigo']:
                articulo={}
                articulo['codigo']= producto['codigo']
                articulo['nombre']= producto['nombre']
                articulo['precio']= producto['precio']
                articulo['cantidad_carrito']= 1
                articulo['cantidad_inventario']= producto['cantidad']
                articulo['precio_total']= producto['precio']
                self.agregar_producto(articulo)
                self.ids.buscar_codigo.text=''
                break


    def agregar_producto(self,articulo):
        self.total+=articulo['precio']
        self.ids.sub_total.text='$ '+"{:.2f}".format(self.total)
        self.ids.rvs.agregar_articulo(articulo)


    def agregar_producto_nombre(self, nombre):
        print("Se mando ", nombre)

    def pagar(self):
        print ("Pagar")

    def  nueva_compra(self):
        print('Nueva Compra')

class VentasApp(App):
    def build(self):
        return VentasWindow()
    

if __name__=='__main__':
    VentasApp().run()