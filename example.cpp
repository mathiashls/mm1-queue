server_state = IDLE;
double sim_time = 0.0;
double next_departure = HUGE_VAL;
double next_arrival = rngl.exp(mean_arrival);

while (sim_time < T_MAX) {

    if(next_arrival < next_departure) {
        sim_time = next_arrival;
        if(server_state == IDLE) {
            server_state = BUSY;
            next_departure = sim_time + rngZ.exp(mean_processing);
        }
        else {
            queue.push( new task(sim_time) );
        }
        next_arrival = sim_time + rngl.exp(mean_arrival);
    }
    else {
        sim_time = next_departure;
        if(queue.empty() ) {
            server_state = IDLE;
            next_departure = HUGE_VAL;
        } else {
            task t = queue.pop();
            next_departure = sim_time + rngZ.exp(mean_processing);
        }
    }

}
