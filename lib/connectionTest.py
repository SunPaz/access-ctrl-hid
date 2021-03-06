from sourceFactory import SourceFactory
import pyodbc  #For MS SQL connection, via odbc

print "PyODBC drivers : "
print str(pyodbc.drivers())

src = SourceFactory('DB', "../cfg/connectionString.sql")
src.loadClientConfiguration(202481600137230)
src.logEvent("Internal test", 1)
print src.getOrCreateClientAccessRight(1, 1)
print src.getOrCreateClientAccessRight(123465789, 1) #New card
