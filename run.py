from flask import Flask
import view

if __name__ == '__main__':
    view.app.run(host="0.0.0.0")
