#include <sstream>

// Include 3rd party headers.
#include <odb/transaction.hxx>
#include <odb/mysql/database.hxx>
#include <bites.hpp>

// Include application headers.
#include "Captor.hpp"
#include "DBWriter.hpp"
#include "mapping.hpp"
#include "mapping-odb.hxx"

namespace wabbit {

void DBWriter::run ()
{
    // Increment the global object count.
    incrCount();

    // Connect to database.    
    odb::mysql::database db (
        m_config["username"],
        m_config["password"],
        m_config["db_name"]
        );

    // Pull from the queue while there are valid tasks.
    Captor::FrameAndTime task;
    m_input_queue.wait_and_pop(task);
    while(task.first)
    {
        // Assemble the time string.
        auto tstring = bites::time2string (
            task.second, 
            "%Y-%m-%d %H:%M:%S.%f"
            );

        // Create the image field.
        wabbit::Image img (tstring);

        // Start the transaction.
        odb::transaction trans (db.begin());

        // Add the image field.
        db.persist(img);

        // Increment the size.
        typedef odb::query<wabbit::Datum> query;
        auto result =
            db.query<wabbit::Datum> (query::name == "size");
        auto datum = result.begin();
        int size = atoi(datum->value().c_str());
        std::stringstream ss;
        ss << size + 1;
        datum->value (ss.str());
        db.update(*datum);

        // Update latest timestamp.
        result = db.query<wabbit::Datum> (query::name == "latest_tstamp");
        datum = result.begin();
        datum->value (tstring);
        db.update(*datum);

        // Commit to database.
        trans.commit();
            
        // Signal done.
        m_done_queue.push (task.first);

        // Pull the next frame.
        m_input_queue.wait_and_pop (task);
    } 

    if (decrCount() != 0)
    {
        // Feed input with "stop" signal.
        m_input_queue.push ({NULL, task.second});
    }
    else
    {
        // Propagate "stop" signal downstream.
    }
}

}  // namespace wabbit.
