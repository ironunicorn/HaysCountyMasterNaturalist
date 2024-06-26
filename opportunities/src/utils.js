import moment from 'moment'

export const CATEGORY_CODES = {
  'PO': 'Public Outreach',
  'DO': 'Direct Outreach',
  'TG': 'Technical Guidance',
  'RM': 'Natural Resource Management',
  'NPA': 'Nature/Public Access',
  'CB': 'Chapter Business',
  'FR': 'Field Research',
  'AT': 'Advanced Training',
  'EV': 'Event',
}

function formatDateTime(unformattedDt) {
  const dt = moment(unformattedDt)
  return dt.format('LT') === '12:00 AM' ?
    '' : dt.format('LT')
}

export function formatDateDisplay(opp) {
  if (opp.anytime) {
    return 'Anytime'
  } else {
    const time = formatDateTime(opp.event_start)
    return opp.event_end ? time.concat(' - ', moment(opp.event_end).format('LT')) : time
  }
}

export function getCategory(category) {
  return CATEGORY_CODES[category]
}

export const DOMAIN = window.location.port === "5173" ?
                        "http://localhost:5000" :
                        ""
