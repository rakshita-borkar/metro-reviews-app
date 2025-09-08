import React, { useState, useEffect } from "react";
import axios from "axios";
import StationSelector from "./components/StationSelector";
import StationHeader from "./components/StationHeader";
import RatingDistribution from "./components/RatingDistribution";
import AspectAnalysis from "./components/AspectAnalysis";
import ReviewList from "./components/ReviewList";
import ReviewFormModal from "./components/ReviewFormModal";
import InsightsBanner from "./components/InsightsBanner";

const App = () => {
  const [stations, setStations] = useState([]);
  const [selectedStation, setSelectedStation] = useState(null);
  const [stationStats, setStationStats] = useState({});
  const [reviews, setReviews] = useState([]);
  const [showReviewForm, setShowReviewForm] = useState(false);

  // Load stations
  useEffect(() => {
    axios.get("/api/stations/").then((res) => {
      setStations(res.data || []);
      if (res.data.length > 0) {
        setSelectedStation(res.data[0]);
      }
    });
  }, []);

  // Load station details when selection changes
  useEffect(() => {
    if (!selectedStation) return;
    axios.get(`/api/stations/${selectedStation.id}/`).then((res) => {
      setStationStats(res.data.stats || {});
      setReviews(res.data.recent_reviews || []);
    });
  }, [selectedStation]);

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-6 grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* Sidebar */}
        <div className="lg:col-span-1">
          <StationSelector
            stations={stations}
            selectedStation={selectedStation}
            onSelect={setSelectedStation}
          />
        </div>

        {/* Main content */}
        <div className="lg:col-span-3 space-y-6">
          {selectedStation && (
            <>
              <StationHeader station={selectedStation} stats={stationStats} />
              <RatingDistribution stats={stationStats} />
              <AspectAnalysis stats={stationStats} />
              <ReviewList
                reviews={reviews}
                onOpenReviewForm={() => setShowReviewForm(true)}
              />
              <InsightsBanner stats={stationStats} />
            </>
          )}
        </div>
      </div>

      {/* Review form modal */}
      {showReviewForm && (
        <ReviewFormModal
          station={selectedStation}
          onClose={() => setShowReviewForm(false)}
        />
      )}
    </div>
  );
};

export default App;
