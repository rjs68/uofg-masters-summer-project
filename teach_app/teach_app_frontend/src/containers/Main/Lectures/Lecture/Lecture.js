import React from 'react';

import LectureVideo from '../../../../components/LectureVideo/LectureVideo';

const lecture = props => (
    <div>
        {props.lecture}
        <LectureVideo />
    </div>
);

export default lecture;