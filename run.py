"""Main script to launch the GrandPy website"""

from application.grandpy.app import app

def launch_app():
	"""Run the application"""
	return app.run(debug=True)

if __name__ == "__main__":
	launch_app()