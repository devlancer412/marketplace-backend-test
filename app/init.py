# Don't edit
__copyright__ = "Copyright 2023"
__license__ = "INTERNAL"
__version__ = "0.0.1"
__status__ = "alpha"


from fastapi import FastAPI
from app.__internal import bootstrap

app = FastAPI(
    title="Marketplace Backend",
    description="Test backend apis of marketplace",
    version="-".join([__version__, __status__]),
    root_path="/",
)

bootstrap(app)