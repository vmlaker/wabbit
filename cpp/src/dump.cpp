/**
   Dump database to stdout.
 */

// Include standard headers.
#include <iostream>
#include <memory>  // std::auto_ptr

// Include 3rd-party headers.
#include <odb/transaction.hxx>
#include <odb/mysql/database.hxx>
#include <bites.hpp>

// Include application headers.
#include "mapping.hpp"
#include "mapping-odb.hxx"

int main (int argc, char** argv)
{
    // Load the configuration file.
    std::string CONFIG = argc >= 2 ? argv[1] : "wabbit.cfg";
    bites::Config config (CONFIG);

    // Connect to database.    
    odb::mysql::database db (
        config["username"],
        config["password"],
        config["db_name"]
        );

    // Dump the contents.
    odb::transaction trans (db.begin());
    odb::result<wabbit::Image> images (db.query<wabbit::Image>());
    for (odb::result<wabbit::Image>::iterator ii = images.begin(); ii != images.end(); ++ii)
    {
        std::cout << ii->id() << " " << ii->time() << std::endl;
    }
    odb::result<wabbit::Datum> data (db.query<wabbit::Datum>());
    for (odb::result<wabbit::Datum>::iterator ii = data.begin(); ii != data.end(); ++ii)
    {
        std::cout << ii->id() << " " << ii->name() << " " << ii->value() << std::endl;
    }
    trans.commit();
}
