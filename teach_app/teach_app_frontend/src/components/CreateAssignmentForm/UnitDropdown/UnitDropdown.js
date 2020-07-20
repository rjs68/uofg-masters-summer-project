import React from 'react';

import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';

const unitDropdown = (props) => {
    var units = []

    if(props.units !== {}){
        for(const unit in props.units){
            units.push(<Dropdown.Item as="button">{props.units[unit]['unit_name']}</Dropdown.Item>);
        }
    }

    return (
        <DropdownButton id="unitSelector" title="Unit">
            {units}
        </DropdownButton>
    )
}

export default unitDropdown;