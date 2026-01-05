from admin import create_app

# 创建Flask应用
app = create_app()

# 启动应用（开发环境）
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)