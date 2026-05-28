
# Dados que já vinham

from flask import render_template, session
from classes.product import Product
from datafile import filename

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import io
import base64

def apps_plot():
    # Creates a pandas dataframe with the orderproduct table data
    engine = create_engine('sqlite:///' + filename + 'business.db')
    df_orderproduct = pd.read_sql('OrderProduct', con=engine)
    # Uses groupby to obtain the total quantity order by product id
    result = df_orderproduct.groupby('product_id')['quantity'].sum()
    # From the product class get the product id names
    p_ids = result.index
    p_names = []
    for p_id in p_ids:
        p_obj = Product.obj[p_id]
        p_names.append(p_obj.name)
    quantities = result.values
    # Uses matplotlib to draw a bar chart
    fig, ax = plt.subplots()
    plt.bar(p_names, quantities, width = 0.4,label = 'Product_id')
    x_index = range(len(p_names))
    plt.xticks(ticks=x_index, labels=p_names)
    plt.xlabel('Product_id')
    plt.ylabel('Quantity')
    plt.title('Total product ordered')
    # Save plot to a bytes buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    image = base64.b64encode(buf.getvalue()).decode('utf-8')
    # Send the image as a Flask response
    return render_template("plot.html", image=image, ulogin=session.get("user"))



#%%

# O que foi "atualizado" por mim

from flask import render_template, session
from classes.product import Product
from datafile import filename

import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import io
import base64


def apps_plot():

    # Creates a pandas dataframe with the orderproduct table data
    engine = create_engine('sqlite:///' + filename + 'business.db')

    df_orderproduct = pd.read_sql('OrderProduct', con=engine)

    # Uses groupby to obtain the total quantity order by product id
    result = df_orderproduct.groupby('product_id')['quantity'].sum()

    # From the product class get the product id names
    p_ids = result.index

    p_names = []

    for p_id in p_ids:
        p_obj = Product.obj[p_id]
        p_names.append(p_obj.name)

    quantities = result.values

    # Uses matplotlib to draw a bar chart

    fig, ax = plt.subplots(figsize=(10,5))
    # Foi adicionado por mim

    plt.bar(
        p_names,
        quantities,
        width=0.4,
        label='Product_id',
        color='skyblue'
    )
    # Foi adicionado por mim (color='skyblue')

    x_index = range(len(p_names))

    plt.xticks(
        ticks=x_index,
        labels=p_names,
        rotation=45
    )
    # Foi adicionado por mim (rotation=45)

    plt.xlabel('Product')
    # Foi alterado/adicionado por mim

    plt.ylabel('Quantity')

    plt.title('Total Products Ordered')
    # Foi alterado/adicionado por mim

    plt.tight_layout()
    # Foi adicionado por mim

    # Save plot to a bytes buffer
    buf = io.BytesIO()

    plt.savefig(buf, format='png')

    plt.close(fig)

    buf.seek(0)

    image = base64.b64encode(
        buf.getvalue()
    ).decode('utf-8')

    # Send the image as a Flask response
    return render_template(
        "plot.html",
        image=image,
        ulogin=session.get("user")
    )