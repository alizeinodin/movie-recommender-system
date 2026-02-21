<?php

return [

    /*
    |--------------------------------------------------------------------------
    | MovieLens user ID range (dataset has 943 users)
    |--------------------------------------------------------------------------
    */
    'user_id_min' => (int) env('RECOMMENDER_USER_ID_MIN', 1),
    'user_id_max' => (int) env('RECOMMENDER_USER_ID_MAX', 943),

];
