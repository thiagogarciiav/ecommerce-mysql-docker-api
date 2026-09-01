from flask import Flask, request, jsonify
from config import Config
from models import db, User, Product, Order, OrderItem
from sqlalchemy import text

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

@app.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': u.id, 'name': u.name, 'email': u.email} for u in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(name=data['name'], email=data['email'])
    db.session.add(user)
    db.session.commit()
    return jsonify({'id': user.id}), 201

@app.route('/products', methods=['GET'])
def list_products():
    name_filter = request.args.get('name')
    query = Product.query
    if name_filter:
        query = query.filter(Product.name.contains(name_filter))
    products = query.all()
    return jsonify([{'id': p.id, 'name': p.name, 'price': str(p.price), 'stock': p.stock} for p in products])

@app.route('/orders', methods=['POST'])
def create_order():
    data = request.json
    user_id = data['user_id']
    items = data['items']  # lista de {product_id, quantity}

    # Cria pedido
    order = Order(user_id=user_id, status='pending')
    db.session.add(order)
    db.session.flush()  # para obter order.id

    # Adiciona itens (as triggers atualizarão estoque e total)
    for item in items:
        product = Product.query.get(item['product_id'])
        if not product:
            db.session.rollback()
            return jsonify({'error': f'Produto {item["product_id"]} não encontrado'}), 404
        if product.stock < item['quantity']:
            db.session.rollback()
            return jsonify({'error': f'Estoque insuficiente para {product.name}'}), 400
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            quantity=item['quantity'],
            unit_price=product.price
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify({'order_id': order.id, 'total': str(order.total)}), 201

@app.route('/reports/sales', methods=['GET'])
def sales_report():
    start = request.args.get('start')
    end = request.args.get('end')
    if not start or not end:
        return jsonify({'error': 'Parâmetros start e end obrigatórios (YYYY-MM-DD)'}), 400
    sql = text("CALL sp_sales_report(:start, :end)")
    result = db.session.execute(sql, {'start': start, 'end': end})
    rows = result.fetchall()
    # O resultado da procedure é um conjunto de resultados; precisamos iterar
    # (para simplificar, convertemos para dicionário)
    output = []
    for row in rows:
        output.append({
            'order_id': row[0],
            'customer': row[1],
            'order_date': str(row[2]),
            'items_count': row[3],
            'total_sales': str(row[4])
        })
    return jsonify(output)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # garante que as tabelas existam (os scripts SQL já criam)
    app.run(host='0.0.0.0', port=5000, debug=True)

@app.route('/')
def home():
    return jsonify({
        'message': 'Bem-vindo à API de e-commerce!',
        'endpoints': {
            'GET /users': 'Lista todos os usuários',
            'POST /users': 'Cria novo usuário',
            'GET /products': 'Lista produtos (filtro opcional ?name=)',
            'POST /orders': 'Cria novo pedido',
            'GET /reports/sales?start=&end=': 'Relatório de vendas'
        }
    })